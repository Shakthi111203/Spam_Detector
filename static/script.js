
async function predictMessage(message) {
    const response = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Prediction failed");
    }

    return data.prediction;
}

async function checkMessage() {
    const message = document.getElementById("message").value;
    const result = document.getElementById("result");

    if (!message.trim()) {
        result.textContent = "Please enter a message.";
        return;
    }

    result.textContent = "Checking...";

    try {
        const prediction = await predictMessage(message);
        result.textContent = "Result: " + prediction;
        result.style.color =
            prediction === "Spam" ? "#dc2626" : "#15803d";
    } catch (error) {
        result.textContent = error.message;
    }
}

async function runTests() {
    const samples = [
        "Congratulations! You have won a free prize. Call now!",
        "Hey, are we meeting for lunch today?",
        "URGENT! You have won a gift card. Claim now!",
        "Please bring the documents to the office tomorrow.",
        "WIN cash now by texting WIN to this number!"
    ];

    const tests = document.getElementById("tests");
    tests.textContent = "Testing messages...";

    try {
        const results = await Promise.all(
            samples.map(async (message) => ({
                message,
                prediction: await predictMessage(message)
            }))
        );

        tests.innerHTML = "<h3>Test Results</h3>";

        results.forEach((item, index) => {
            const row = document.createElement("p");
            row.textContent =
                (index + 1) + ". " + item.message +
                " → " + item.prediction;
            tests.appendChild(row);
        });
    } catch (error) {
        tests.textContent = error.message;
    }
}
