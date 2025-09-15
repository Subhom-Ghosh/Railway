function postScan(fittingId) {
    fetch('/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fitting_id: fittingId })
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById('result');
        if (data.error) {
            resultDiv.innerHTML = `<p style="color:red;">${data.error}</p>`;
        } else {
            resultDiv.innerHTML = `
                <h2>Fitting Details</h2>
                <p><b>ID:</b> ${data.fitting_id}</p>
                <p><b>Vendor:</b> ${data.vendor}</p>
                <p><b>Supply Date:</b> ${data.supply_date}</p>
                <p><b>Warranty Period (months):</b> ${data.warranty_period_months}</p>
                <p><b>Inspection Dates:</b> ${data.inspection_dates.join(', ')}</p>
                <p><b>Failure Count:</b> ${data.failure_count}</p>
                <h3>Alerts</h3>
                <ul>${data.alerts.map(alert => `<li>${alert}</li>`).join('')}</ul>
            `;
        }
    });
}

function startScanner() {
    const html5QrcodeScanner = new Html5QrcodeScanner(
        "qr-reader", { fps: 10, qrbox: 250 });

    html5QrcodeScanner.render(
        (decodedText, decodedResult) => {
            try {
                const parsed = JSON.parse(decodedText);
                postScan(parsed.fitting_id);
            } catch (e) {
                postScan(decodedText);  // fallback: treat text as fitting_id
            }
            html5QrcodeScanner.clear();
        },
        (errorMessage) => { console.warn(`QR error: ${errorMessage}`); }
    );
}

window.onload = startScanner;
