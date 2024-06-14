document.addEventListener("DOMContentLoaded", async () => {
  const uploadPDF = document.getElementById("uploadPDF");
  const signaturePad = document.getElementById("signaturePad");
  const clearSignature = document.getElementById("clearSignature");
  const addSignature = document.getElementById("addSignature");
  const pdfCanvas = document.getElementById("pdfCanvas");
  const context = signaturePad.getContext("2d");
  const pdfContext = pdfCanvas.getContext("2d");

  let pdfDoc = null;
  let signatureImage = null;
  let isDrawing = false;
  let signaturePosition = { x: 0, y: 0 };
  let selectedPage = 0;
  let templateImage = null;

  // Inisialisasi PDF.js
  await initPDFJS();

  // Function untuk menginisialisasi PDF.js
  async function initPDFJS() {
    const pdfjsLib = window["pdfjs-dist/build/pdf"];
    pdfjsLib.GlobalWorkerOptions.workerSrc =
      "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.7.570/pdf.worker.min.js";
  }

  // Function untuk membersihkan signature pad
  clearSignature.addEventListener("click", () => {
    context.clearRect(0, 0, signaturePad.width, signaturePad.height);
  });

  // Mengatur fungsi untuk menggambar pada signature pad
  signaturePad.addEventListener("mousedown", () => (isDrawing = true));
  signaturePad.addEventListener("mouseup", () => (isDrawing = false));
  signaturePad.addEventListener("mouseout", () => (isDrawing = false));
  signaturePad.addEventListener("mousemove", draw);

  function draw(event) {
    if (!isDrawing) return;

    context.lineWidth = 2;
    context.lineCap = "round";
    context.strokeStyle = "#000";

    context.lineTo(event.offsetX, event.offsetY);
    context.stroke();
    context.beginPath();
    context.moveTo(event.offsetX, event.offsetY);
  }

  // Menangani unggah PDF
  uploadPDF.addEventListener("change", async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      const arrayBuffer = await file.arrayBuffer();
      pdfDoc = await PDFLib.PDFDocument.load(arrayBuffer);
      await renderPDF(arrayBuffer);
    } catch (error) {
      console.error("Error loading PDF:", error);
      alert("Terjadi kesalahan saat memuat PDF.");
    }
  });

  // Render PDF pada canvas
  async function renderPDF(arrayBuffer) {
    try {
      const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
      const pdf = await loadingTask.promise;

      const pagePrompt = prompt(
        `Masukkan nomor halaman (1-${pdf.numPages}):`,
        "1"
      );
      selectedPage = parseInt(pagePrompt) - 1;

      if (
        isNaN(selectedPage) ||
        selectedPage < 0 ||
        selectedPage >= pdf.numPages
      ) {
        alert("Nomor halaman tidak valid atau melebihi batas!");
        return;
      }

      const page = await pdf.getPage(selectedPage + 1);
      const viewport = page.getViewport({ scale: 1 });
      pdfCanvas.width = viewport.width;
      pdfCanvas.height = viewport.height; // Menyesuaikan ukuran canvas dengan ukuran viewport PDF

      const renderContext = {
        canvasContext: pdfContext,
        viewport: viewport,
      };

      await page.render(renderContext).promise;
    } catch (error) {
      console.error("Error rendering PDF:", error);
      alert("Terjadi kesalahan saat merender PDF.");
    }
  }

  // Menangani klik pada canvas PDF
  pdfCanvas.addEventListener("click", (event) => {
    const rect = pdfCanvas.getBoundingClientRect();
    signaturePosition.x = event.clientX - rect.left;
    signaturePosition.y = event.clientY - rect.top;
  });

  // Menangani unggah template
  uploadTemplate.addEventListener("change", async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      templateImage = await loadImage(file);
      addTemplateToCanvas();
    } catch (error) {
      console.error("Error loading template:", error);
      alert("Terjadi kesalahan saat memuat template.");
    }
  });

  // Load gambar dari file
  function loadImage(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (event) => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = reject;
        img.src = event.target.result;
      };
      reader.readAsDataURL(file);
    });
  }

  // Menambahkan template ke canvas
  function addTemplateToCanvas() {
    if (!templateImage) {
      alert("Harap unggah file template terlebih dahulu.");
      return;
    }

    const ratio = Math.min(
      signaturePad.width / templateImage.width,
      signaturePad.height / templateImage.height
    );
    const newWidth = templateImage.width * ratio;
    const newHeight = templateImage.height * ratio;

    signaturePad.width = newWidth;
    signaturePad.height = newHeight;
    context.drawImage(templateImage, 0, 0, newWidth, newHeight);
  }

  // Menambahkan signature ke PDF
  addSignature.addEventListener("click", async () => {
    if (!pdfDoc) {
      alert("Harap unggah file PDF terlebih dahulu.");
      return;
    }

    try {
      const tempCanvas = document.createElement("canvas");
      const tempContext = tempCanvas.getContext("2d");
      tempCanvas.width = signaturePad.width;
      tempCanvas.height = signaturePad.height;
      tempContext.drawImage(signaturePad, 0, 0);

      signatureImage = tempCanvas.toDataURL("image/png");

      const pages = pdfDoc.getPages();
      const selectedPageObj = pages[selectedPage];

      const pngImageBytes = await fetch(signatureImage).then((res) =>
        res.arrayBuffer()
      );
      const pngImage = await pdfDoc.embedPng(pngImageBytes);

      const pngDims = pngImage.scale(0.5);

      selectedPageObj.drawImage(pngImage, {
        x: signaturePosition.x,
        y: selectedPageObj.getHeight() - signaturePosition.y - pngDims.height,
        width: pngDims.width,
        height: pngDims.height,
      });

      const pdfBytes = await pdfDoc.save();
      download(pdfBytes, "signed.pdf", "application/pdf");
    } catch (error) {
      console.error("Error adding signature to PDF:", error);
      alert("Terjadi kesalahan saat menambahkan tanda tangan ke PDF.");
    }
  });

  // Fungsi pembantu untuk mengunduh PDF yang ditandatangani
  function download(data, filename, type) {
    const blob = new Blob([data], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    }, 0);
  }
});
