# PlacementPro

Placement management API built with FastAPI, SQLAlchemy, SQLite and JWT authentication.

## Run
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
- Frontend: http://127.0.0.1:8000/
- Swagger docs: http://127.0.0.1:8000/docs
- Demo admin (demo only): admin@placementpro.com / Admin@123

## Roles
- **Student**: manages own profile, searches jobs, checks eligibility, applies, tracks applications
- **Recruiter**: posts jobs, views applicants for own jobs, updates application status
- **Admin (Placement Officer)**: approves jobs, views students and platform stats

## Endpoints
- Auth: `POST /auth/register`, `POST /auth/login`
- Students: `GET/PUT /students/me/profile`, `GET /students`
- Jobs: `POST /jobs`, `GET /jobs` (filters: q, job_type, location, company, min_package, skip, limit), `GET/PUT/DELETE /jobs/{job_id}`, `PATCH /jobs/{job_id}/approve`, `GET /jobs/{job_id}/eligibility`
- Applications: `POST /applications`, `GET /applications/me`, `GET /applications/job/{job_id}`, `PATCH /applications/{app_id}/status`, `DELETE /applications/{app_id}`
- Admin: `GET /admin/stats`

## Business rules
- Only student and recruiter roles can self-register
- Eligibility is checked against each job's minimum CGPA, allowed branches, maximum backlogs and deadline
- A student cannot apply to the same job twice (409)
- Status flow: applied, shortlisted, interview_scheduled, selected / rejected. Invalid moves return 400
- Protected endpoints return 401 without a token and 403 for the wrong role