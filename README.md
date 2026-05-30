# Apache Airflow Setup Guide
> A beginner-friendly guide to running Apache Airflow locally using Docker.

---

## Prerequisites

Before starting, make sure you have the following installed on your machine:

| Tool | Why you need it | Install Link |
|------|----------------|--------------|
| Docker Desktop | Runs all Airflow services in containers | [docker.com](https://www.docker.com/products/docker-desktop) |
| Docker Compose | Manages multi-container setup (comes with Docker Desktop) | Included above |
| curl | Downloads files from the terminal | Pre-installed on Mac/Linux. Windows: use Git Bash |

To verify everything is ready, run:
```bash
docker --version
docker compose version
```
Both commands should return a version number. If not, revisit the installs above.

---

## Step 1 — Download the Official docker-compose.yaml

Run this command to download the official Airflow Docker Compose file:

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
```

> ⚠️ This downloads the file directly into your current directory. Make sure you're inside your project folder before running it.

📖 If the command doesn't work, you can manually download it from the [Official Airflow Docs](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).

---

## Step 2 — Expose the PostgreSQL Port

By default, the PostgreSQL database inside Docker is not accessible from your local machine. To expose it:

1. Open `docker-compose.yaml` in any text editor
2. Find the `postgres:` service block (search with `Ctrl+F` → type `postgres:`)
3. Add the `ports` section under it:

```yaml
postgres:
  image: postgres:13
  ports:
    - "5432:5432"   # ← Add this line
```

> 💡 This maps port 5432 inside Docker to port 5432 on your machine, so tools like DBeaver or TablePlus can connect to it.

---

## Step 3 — Create the .env File

Airflow needs a few environment variables to run correctly. Create a `.env` file in the **same folder** as your `docker-compose.yaml`:

```bash
# On Mac/Linux
touch .env
```

Then open it and add:

```env
AIRFLOW_UID=50000
AIRFLOW_PROJ_DIR=.
```

> 💡 `AIRFLOW_UID` sets the user ID inside the container. `50000` is the recommended default. On Linux, you can use your own UID by running `echo $(id -u)`.

---

## Step 4 — Create the Required Project Folders

Airflow expects these 4 folders to exist before it starts:

```bash
mkdir -p dags plugins logs config
```

| Folder | Purpose |
|--------|---------|
| `dags/` | Place your DAG Python files here |
| `plugins/` | Custom Airflow plugins |
| `logs/` | Task execution logs |
| `config/` | Airflow configuration overrides |

---

## Step 5 — Auto-Create Extra Working Folders (Optional but Recommended)

For MLOps workflows, you'll want extra folders like `artifacts/`, `data/`, `models/`, and `outputs/` to be created automatically every time Airflow initializes — so nothing breaks if someone clones your repo fresh.

Open `docker-compose.yaml`, find the `airflow-init:` service block, and **replace** its `entrypoint` with this:

```yaml
airflow-init:
  <<: *airflow-common
  command: version
  entrypoint:
    - /bin/bash
    - -c
    - |
      # Create all required working directories at once
      mkdir -p /opt/airflow/artifacts /opt/airflow/data /opt/airflow/models /opt/airflow/outputs

      # Grant full read/write permissions to all folders
      chmod 777 /opt/airflow/artifacts /opt/airflow/data /opt/airflow/models /opt/airflow/outputs

      exec /entrypoint version
```

> 💡 To add more folders later, just append them to the `mkdir -p` and `chmod 777` lines separated by a space.

---

## Step 6 — Start Airflow

**First time only** — initialize the database:

```bash
docker compose up airflow-init
```

Wait for the logs to show `exited with code 0` — that means initialization was successful.

Then start all Airflow services:

```bash
docker compose up -d
```

The `-d` flag runs everything in the background (detached mode).

---

## Step 7 — Access the Airflow UI

Once all containers are running, open your browser and go to:

```
http://localhost:8080
```

Default login credentials:

| Field | Value |
|-------|-------|
| Username | `airflow` |
| Password | `airflow` |

---

## Common Commands

```bash
# Stop all Airflow services
docker compose down

# Restart after making changes to docker-compose.yaml
docker compose down
docker compose up -d

# View running containers
docker ps

# Check logs for a specific service
docker compose logs airflow-webserver
```

---

## Project Structure

After setup, your project folder should look like this:

```
your-project/
├── dags/               ← Your DAG files go here
├── plugins/            ← Custom plugins
├── logs/               ← Auto-generated task logs
├── config/             ← Airflow config overrides
├── artifacts/          ← Auto-created by entrypoint
├── data/               ← Auto-created by entrypoint
├── models/             ← Auto-created by entrypoint
├── outputs/            ← Auto-created by entrypoint
├── .env                ← Environment variables
└── docker-compose.yaml ← Main config file
```

---

## Troubleshooting

**Problem: Port 5432 already in use**
> You have a local PostgreSQL running. Either stop it or change the port in `docker-compose.yaml` to `"5433:5432"`.

**Problem: `docker compose up` fails immediately**
> Run `docker compose up airflow-init` first. Skipping this step is the most common mistake.

**Problem: DAGs not showing in UI**
> Make sure your `.py` DAG files are inside the `dags/` folder. Airflow scans this folder every 30 seconds.

**Problem: Permission denied on folders**
> Re-run `docker compose down` then `docker compose up -d`. The entrypoint will recreate the folders with correct permissions.
