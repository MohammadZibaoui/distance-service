# distance-service (VisitaUp)

## Descrição

Serviço autônomo que calcula a distância (em km) entre duas coordenadas geográficas.

## Endpoints

- `POST /distance` — body: `{ "from": {"lat":..., "lon":...}, "to": {"lat":..., "lon":...} }` → `{ "distance_km": float }`
- `POST /distance/batch` — batch de pares
- `GET /health` — status
- `GET /metrics` — métricas simples (req_count, avg_latency_ms)

## Como rodar local

1. `python -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `python distance_service.py` (o serviço executará em `http://127.0.0.1:5000`)

## Docker

Build: `docker build -t distance-service:local .`
Run: `docker run -p 5000:5000 distance-service:local`

