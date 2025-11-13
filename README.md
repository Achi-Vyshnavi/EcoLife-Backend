# EcoLife-Backend
A simple FastAPI backend that tracks energy usage and calculates carbon footprint.

### Features
- Create and manage users  
- Log energy, travel, and food activity data  
- Calculate total carbon footprint  
- API auto-documented with Swagger UI

### Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
Open in browser: http://127.0.0.1:8000/docs


---

Once you add all four files and commit them, your backend is **ready to deploy**.

Next step 👉 go to **Render.com** and deploy using:
- **Build command:** `pip install -r requirements.txt`  
- **Start command:** `uvicorn main:app --host 0.0.0.0 --port 10000`  
- **Environment variable:**  


DATABASE_URL = sqlite:///./ecolife.db
