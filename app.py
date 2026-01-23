import requests
import json

url = "https://api.kie.ai/api/v1/jobs/createTask"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 733649a9b1c750cb2caf2631855d9222"
}

payload = {
    "model": "grok-imagine/text-to-video",
    "callBackUrl": "https://fbreeldown.streamlit.app/api/callback",
    "input": {
        "prompt": "A couple of doors open to the right one by one randomly and stay open, to show the inside, each is either an living room, or a kitchen, or a bedroom or an office, with little people living inside.",
        "aspect_ratio": "2:3",
        "mode": "normal"
    }
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
result = response.json()
print(result)
