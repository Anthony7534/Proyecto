from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.routes import temperatura_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: ["http://localhost", "http://127.0.0.1"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir el router de temperatura_router con la etiqueta 'Conversiones de Temperaturas'
app.include_router(temperatura_router, tags=["Conversiones de Temperaturas"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
