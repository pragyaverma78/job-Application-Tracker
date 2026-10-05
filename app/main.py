from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import Application, ApplicationCreate

app = FastAPI(title="Job Application Tracker API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

applications = [
    Application(id=1, company="Google", role="Software Engineer", status="Applied", applied_date="2026-09-20"),
    Application(id=2, company="Amazon", role="Frontend Developer", status="Interview", applied_date="2026-09-24"),
]
next_id = 3

@app.get("/")
def root():
    return {"message": "Job Application Tracker API is running"}

@app.get("/applications", response_model=list[Application])
def get_applications():
    return applications

@app.post("/applications", response_model=Application, status_code=201)
def create_application(data: ApplicationCreate):
    global next_id
    item = Application(id=next_id, **data.model_dump())
    applications.append(item)
    next_id += 1
    return item

@app.delete("/applications/{application_id}")
def delete_application(application_id: int):
    for i, item in enumerate(applications):
        if item.id == application_id:
            applications.pop(i)
            return {"message": "Application deleted"}
    raise HTTPException(status_code=404, detail="Application not found")

@app.get("/stats")
def stats():
    return {
        "total": len(applications),
        "applied": sum(x.status == "Applied" for x in applications),
        "interview": sum(x.status == "Interview" for x in applications),
        "selected": sum(x.status == "Selected" for x in applications),
        "rejected": sum(x.status == "Rejected" for x in applications),
    }
