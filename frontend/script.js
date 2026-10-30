
const API_URL = "http://54.173.15.1:8000";

async function shortenUrl(e) {
  e.preventDefault();
  
  const originalUrl = document.getElementById("originalUrl").value;
  const submitBtn = document.getElementById("submitBtn");
  const resultContainer = document.getElementById("resultContainer");
  const errorMessage = document.getElementById("errorMessage");

  // Estado de carga
  submitBtn.disabled = true;
  submitBtn.innerHTML = `<i class="fa-solid fa-spinner animate-spin"></i> Procesando...`;
  errorMessage.classList.add("hidden");
  resultContainer.classList.add("hidden");

  try {
    const response = await fetch(`${API_URL}/shorten`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ original_url: originalUrl })
    });

    if (!response.ok) {
      throw new Error("Ocurrió un error al procesar la solicitud en la API.");
    }

    const data = await response.json();

    // Mostrar resultados
    document.getElementById("shortUrlInput").value = data.short_url;
    document.getElementById("testLink").href = data.short_url;
    resultContainer.classList.remove("hidden");

  } catch (error) {
    document.getElementById("errorText").innerText = error.message || "No se pudo conectar con el backend en EC2.";
    errorMessage.classList.remove("hidden");
  } finally {
    // Restaurar botón
    submitBtn.disabled = false;
    submitBtn.innerHTML = `<span>Acortar URL</span> <i class="fa-solid fa-wand-magic-sparkles"></i>`;
  }
}

function copyToClipboard() {
  const copyInput = document.getElementById("shortUrlInput");
  copyInput.select();
  navigator.clipboard.writeText(copyInput.value);

  const copyText = document.getElementById("copyText");
  copyText.innerText = "¡Copiado!";
  setTimeout(() => {
    copyText.innerText = "Copiar";
  }, 2000);
}