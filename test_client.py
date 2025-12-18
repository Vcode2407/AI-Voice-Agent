import asyncio
import websockets
import json

async def test_telugu_agent():
    uri = "ws://localhost:3000/ws"
    
    print("Connecting to agent...")
    async with websockets.connect(uri) as websocket:
        # Scenario 1: Successful case
        print("\n=== Test 1: Farmer seeking schemes ===")
        
        # Simulate user saying this in Telugu
        message = {
            "type": "response.create",
            "response": {
                "modalities": ["text"],
                "instructions": "User said: నాకు 30 సంవత్సరాలు. నేను రైతును. నా రాష్ట్రం ఆంధ్ర ప్రదేశ్. నా ఆదాయం సంవత్సరానికి 50000 రూపాయలు."
            }
        }
        
        await websocket.send(json.dumps(message))
        
        # Receive response
        async for response in websocket:
            data = json.loads(response)
            print(f"Response: {data}")
            if data.get("type") == "response.done":
                break

asyncio.run(test_telugu_agent())
