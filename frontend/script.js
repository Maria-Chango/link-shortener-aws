const API_BASE_URL = "http://<IP-PUBLICA-EC2>:8000";

async function shortenUrl() {
    const urlInput = document.getElementById("urlInput").value;
    const errorContainer = document.getElementById("errorContainer");
    const resultContainer = document.getElementById("resultContainer");

    // Limpiar estados anteriores
    errorContainer.classList.add("hidden");
    resultContainer.classList.add("hidden");

    if (!urlInput) {
        showError("Por favor, ingresa una URL válida.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/shorten`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ original_url: urlInput })
        });

        if (!response.ok) {
            throw new Error("Error en la respuesta del servidor.");
        }

        const data = await response.json();
        
        document.getElementById("shortUrlOutput").value = data.short_url;
        document.getElementById("visitLink").href = data.short_url;
        resultContainer.classList.remove("hidden");

    } catch (error) {
        showError("No se pudo conectar con el backend en EC2. Verifica que la API esté activa y CORS configurado.");
        console.error(error);
    }
}

function copyToClipboard() {
    const copyText = document.getElementById("shortUrlOutput");
    copyText.select();
    document.execCommand("copy");
    alert("¡Enlace copiado al portapapeles!");
}

function showError(message) {
    const errorContainer = document.getElementById("errorContainer");
    errorContainer.textContent = message;
    errorContainer.classList.remove("hidden");
}