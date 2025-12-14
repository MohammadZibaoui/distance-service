# distance_service.py
from flask import Flask, request, jsonify
import math
import time

app = Flask(__name__)

# métricas em memória
metrics = {"req_count": 0, "total_time_ms": 0.0}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@app.route("/distance", methods=["POST"])
def distance():
    start = time.time()
    body = request.get_json(force=True)
    if not body:
        return jsonify({"error": "invalid body"}), 400
    f = body.get("from") or body.get("origin")
    t = body.get("to") or body.get("destination")
    if not f or not t:
        return jsonify({"error": "missing origin or destination"}), 400
    try:
        lat1, lon1 = float(f["lat"]), float(f["lon"])
        lat2, lon2 = float(t["lat"]), float(t["lon"])
    except Exception:
        return jsonify({"error": "invalid coordinates"}), 400
    d = haversine(lat1, lon1, lat2, lon2)
    elapsed = (time.time() - start) * 1000
    metrics["req_count"] += 1
    metrics["total_time_ms"] += elapsed
    return jsonify({"distance_km": round(d, 4), "units": "km"})

@app.route("/distance/batch", methods=["POST"])
def distance_batch():
    body = request.get_json(force=True)
    items = body.get("pairs", [])
    results = []
    for p in items:
        f = p.get("from")
        t = p.get("to")
        results.append({"from": f, "to": t, "distance_km": haversine(float(f["lat"]), float(f["lon"]), float(t["lat"]), float(t["lon"]))})
    return jsonify({"results": results})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/metrics", methods=["GET"])
def get_metrics():
    avg = metrics["total_time_ms"] / metrics["req_count"] if metrics["req_count"] > 0 else 0
    return jsonify({"req_count": metrics["req_count"], "avg_latency_ms": avg})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
