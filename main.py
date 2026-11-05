from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from google.ads.googleads.client import GoogleAdsClient
import os

app = FastAPI()

# Carrega as configurações do Google Ads do .env
config = {
    "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
    "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
    "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
    "refresh_token": os.getenv("GOOGLE_ADS_CLIENT_REFRESH_TOKEN"),
    "use_proto_plus": True,
}

@app.get("/api/metrics")
def get_metrics():
    try:
        client = GoogleAdsClient.load_from_dict(config)
        ga_service = client.get_service("GoogleAdsService")
        customer_id = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
        
        query = """
            SELECT
              campaign.id,
              campaign.name,
              metrics.impressions,
              metrics.clicks,
              metrics.cost_micros,
              metrics.conversions
            FROM campaign
            WHERE segments.date DURING LAST_30_DAYS
        """
        response = ga_service.search(customer_id=customer_id, query=query)
        
        campaigns = []
        for row in response:
            campaigns.append({
                "name": row.campaign.name,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "cost": row.metrics.cost_micros / 1_000_000,
                "conversions": row.metrics.conversions
            })
        return {"status": "success", "data": campaigns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str.format("Erro na API: {}", str(e)))

@app.get("/", response_class=HTMLResponse)
def dashboard_home():
    return """
    <html>
        <head>
            <title>Painel de Anúncios</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-100 p-8">
            <div class="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow">
                <h1 class="text-2xl font-bold text-gray-800 mb-4">Painel de Métricas do Google Ads</h1>
                <p class="text-gray-600">Seu painel web está ativo e conectado com sucesso!</p>
            </div>
        </body>
    </html>
    """
