from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageData(BaseModel):
    image_base64: str


@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

async def agent_llm_stream(base64_str: str):
    await asyncio.sleep(0.5) 
    
    mock_words = ["正", "前", "方", "发", "现", "了", "一", "个", "水", "杯", "。"]
    for word in mock_words:
        msg = json.dumps({"type": "text", "content": word}, ensure_ascii=False)
        yield f"data: {msg}\n\n"
        await asyncio.sleep(0.1) 
        
    area_ratio = 0.6 
    vibration_level = max(1, min(10, int(area_ratio * 10))) 
    
    vib_msg = json.dumps({"type": "vibration", "level": vibration_level})
    yield f"data: {vib_msg}\n\n"
    yield "data: [DONE]\n\n"

@app.post("/api/v1/vision")
async def vision_endpoint(payload: ImageData):
    print(f"✅ 收到端侧图片，大小为: {len(payload.image_base64)} 字节")
    return StreamingResponse(agent_llm_stream(payload.image_base64), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)