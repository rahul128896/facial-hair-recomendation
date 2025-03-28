// Tab functionality
document.addEventListener("DOMContentLoaded", () => {
    // Tab switching
    const tabBtns = document.querySelectorAll(".tab-btn")
    const tabContents = document.querySelectorAll(".tab-content")
  
    tabBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        // Remove active class from all buttons and contents
        tabBtns.forEach((b) => b.classList.remove("active"))
        tabContents.forEach((c) => c.classList.remove("active"))
  
        // Add active class to clicked button and corresponding content
        btn.classList.add("active")
        const tabId = btn.getAttribute("data-tab")
        document.getElementById(`${tabId}-tab`).classList.add("active")
      })
    })
  
    // File upload functionality
    const fileInput = document.getElementById("fileInput")
    if (fileInput) {
      fileInput.addEventListener("change", previewFile)
    }
  
    const uploadForm = document.getElementById("uploadForm")
    if (uploadForm) {
      uploadForm.addEventListener("submit", (event) => {
        event.preventDefault()
        uploadFile()
      })
    }
  
    // Camera functionality
    const video = document.getElementById("video")
    if (video) {
      // Initialize webcam
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
          .getUserMedia({ video: true })
          .then((stream) => {
            video.srcObject = stream
            video.play()
          })
          .catch((error) => {
            console.error("Error accessing webcam:", error)
            alert("Webcam access denied or not available!")
          })
      }
    }
  
    const captureBtn = document.getElementById("captureBtn")
    if (captureBtn) {
      captureBtn.addEventListener("click", captureImage)
    }
  })
  
  function uploadFile() {
    const fileInput = document.getElementById("fileInput")
    const file = fileInput.files[0]
  
    if (!file) {
      alert("Please select a file!")
      return
    }
  
    const formData = new FormData()
    formData.append("file", file)
  
    // Show loading state
    const submitBtn = document.querySelector('#uploadForm button[type="submit"]')
    submitBtn.textContent = "Analyzing..."
    submitBtn.disabled = true
  
    fetch("/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.redirected) {
          window.location.href = response.url
        } else {
          return response.json()
        }
      })
      .then((data) => {
        if (data && data.error) {
          alert(data.error)
          // Reset button
          submitBtn.textContent = "Analyze"
          submitBtn.disabled = false
        }
      })
      .catch((error) => {
        console.error("Error:", error)
        // Reset button
        submitBtn.textContent = "Analyze"
        submitBtn.disabled = false
      })
  }
  
  function captureImage() {
    const video = document.getElementById("video")
    const canvas = document.getElementById("canvas")
    const captureBtn = document.getElementById("captureBtn")
  
    if (!video || !canvas) return
  
    const context = canvas.getContext("2d")
  
    // Set canvas size to match video
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
  
    // Draw the video frame onto the canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height)
  
    // Convert canvas image to data URL
    const imageData = canvas.toDataURL("image/jpeg")
  
    // Show loading state
    captureBtn.textContent = "Analyzing..."
    captureBtn.disabled = true
  
    // Send image data to the backend
    fetch("/capture", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: "image=" + encodeURIComponent(imageData),
    })
      .then((response) => {
        if (response.redirected) {
          window.location.href = response.url
        } else {
          alert("Capture failed!")
          // Reset button
          captureBtn.textContent = "Capture & Analyze"
          captureBtn.disabled = false
        }
      })
      .catch((error) => {
        console.error("Error capturing image:", error)
        // Reset button
        captureBtn.textContent = "Capture & Analyze"
        captureBtn.disabled = false
      })
  }
  
  function previewFile() {
    const fileInput = document.getElementById("fileInput")
    const file = fileInput.files[0]
    const previewImage = document.getElementById("previewImage")
    const previewVideo = document.getElementById("previewVideo")
    const fileLabel = document.querySelector(".file-text")
  
    if (file) {
      const fileURL = URL.createObjectURL(file)
      fileLabel.textContent = file.name
  
      if (file.type.startsWith("image")) {
        previewVideo.style.display = "none"
        previewImage.style.display = "block"
        previewImage.src = fileURL
      } else if (file.type.startsWith("video")) {
        previewImage.style.display = "none"
        previewVideo.style.display = "block"
        previewVideo.src = fileURL
      }
    }
  }
  
  