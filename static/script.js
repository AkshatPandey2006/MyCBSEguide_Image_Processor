document.getElementById("uploadForm").onsubmit = async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch("/process", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    const downloadSection = document.getElementById("downloadSection");
    const downloadLink = document.getElementById("downloadLink");
    
    downloadLink.href = data.processed_image_url;
    downloadSection.style.display = "block";
};
