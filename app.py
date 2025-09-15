
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Load mock data
with open('fittings_data.json') as f:
    MOCK_FITTINGS = json.load(f)

def check_fitting_status(fitting):
    alerts = []
    supply_date = datetime.strptime(fitting['supply_date'], "%Y-%m-%d")
    warranty_expiry = supply_date + timedelta(days=30 * fitting['warranty_period_months'])

    if datetime.today() > warranty_expiry:
        alerts.append("⚠️ Warranty Expired")

    if fitting['failure_count'] > 1:
        alerts.append("⚠️ Multiple Failures – At Risk")

    return alerts

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    fitting_id = data.get('fitting_id')

    if fitting_id not in MOCK_FITTINGS:
        return jsonify({"error": "Fitting not found"}), 404

    fitting = MOCK_FITTINGS[fitting_id]
    alerts = check_fitting_status(fitting)

    return jsonify({
        "fitting_id": fitting_id,
        "vendor": fitting['vendor'],
        "supply_date": fitting['supply_date'],
        "warranty_period_months": fitting['warranty_period_months'],
        "inspection_dates": fitting['inspection_dates'],
        "failure_count": fitting['failure_count'],
        "alerts": alerts
    })

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

