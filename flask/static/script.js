document.getElementById("predict-form").addEventListener("submit", function (event) {
    event.preventDefault();

    let userId = document.getElementById("user_id").value;

    fetch("/predict", {
        method: "POST",
        body: new URLSearchParams({ user_id: userId }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })
    .then(response => response.json())
    .then(data => {
        let score = data.prediction;
        document.getElementById("score").textContent = score;

        // Animate Circular Fill
        let maxScore = 900;
        let minScore = 300;
        let percent = (score - minScore) / (maxScore - minScore);
        let dashOffset = 283 - (283 * percent);
        document.querySelector(".progress-circle").style.strokeDashoffset = dashOffset;
    })
    .catch(error => console.error("Error:", error));
});
