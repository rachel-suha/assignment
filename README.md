# PlacementPro

Placement management API built with FastAPI, SQLAlchemy, PostgreSQL/Supabase (or SQLite locally) and JWT authentication.

## Run
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```
- Frontend: http://127.0.0.1:8000/
- Swagger docs: http://127.0.0.1:8000/docs

## Supabase setup
1. Run `supabase_schema.sql` in the Supabase SQL Editor.
2. In Supabase, open **Project Settings > Database** and copy the PostgreSQL connection URI. Use the session pooler URI if your network cannot connect to the direct database host.
3. Put the URI in `.env` as `DATABASE_URL`. Keep `?sslmode=require` in the URI; replace its password placeholder with your database password (URL-encode special characters in the password).
4. Set `ADMIN_EMAIL` and `ADMIN_PASSWORD` in `.env` to provision the placement-officer account. Use a strong password. The app updates that account's password hash at startup from these values.

Example `.env` values:
```
DATABASE_URL=postgresql://postgres:YOUR_DB_PASSWORD@db.YOUR_PROJECT_REF.supabase.co:5432/postgres?sslmode=require
ADMIN_EMAIL=placement-officer@example.com
ADMIN_PASSWORD=replace-with-a-strong-password
```

If `DATABASE_URL` is omitted, the app uses the local `placementpro.db` SQLite file. Never commit `.env` or share its database password.

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