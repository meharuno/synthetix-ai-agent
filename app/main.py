from fastapi import FastAPI, Request
import httpx  

app = FastAPI()
N8N_WEBHOOK_URL =  "https://meharunissa.app.n8n.cloud/webhook-test/ea29512d-75f7-444c-8fc1-6ae3e8743625"  # replace with actual webhook
@app.post("/send-to-n8n")
async def send_to_n8n(request: Request):
    data = await request.json()

    async with httpx.AsyncClient() as client:
        response = await client.post(N8N_WEBHOOK_URL, json=data)

    return {"status": "sent to n8n", "n8n_response": response.text}
