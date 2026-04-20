document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.querySelector('form');
    if(uploadForm){
        uploadForm.addEventListener('submit', (e) => {
            const fileInput = uploadForm.querySelector('input[type="file"]');
            if(!fileInput.files.length){
                alert("Please select a resume to upload!");
                e.preventDefault();
            }
        });
    }
});
