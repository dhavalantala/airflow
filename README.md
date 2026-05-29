# Airflow Setup Guide

## 1. Download docker-compose.yaml
Run the following command to download the official Apache Airflow Docker Compose file:

👉 **[Official Download Documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)** if you need to fetch the file manually from the web.

```bash
curl -Lf 'https://apache.org' -o docker-compose.yaml
```



## 2. Configure PostgreSQL Port
Open the downloaded `docker-compose.yaml` file, locate line number 102 under the `postgres` service configuration, and expose the port by adding or changing the value to:

```yaml
    ports:
      - "5432:5432"
```

## 3. Create .env File
Create a `.env` file in your root directory and add the following environment variables:

```env
AIRFLOW_UID=50000
AIRFLOW_PROJ_DIR=.
```
## 4. Create Project Folders
Run the following command in your terminal to create the 4 required Airflow directories:

```bash
mkdir -p dags plugins logs config
```

## 5. Start Airflow
Initialize the database and start the containers using these commands:

```bash
# Initialize the database
docker compose up airflow-init

# Start all Airflow services
docker compose up -d
```

```bash
docker compose down
docker compose up -d
```

I want the `artifacts` folder to be created automatically. 
```bash
entrypoint:
      - /bin/bash
      - -c
      - |
        mkdir -p /opt/airflow/artifacts
        chmod 777 /opt/airflow/artifacts
        exec /entrypoint version
```

To create multiple folders automatically, you can add them to the same mkdir and chmod lines inside the entrypoint 
```bash
  airflow-init:
    <<: *airflow-common
    command: version
    entrypoint:
      - /bin/bash
      - -c
      - |
        # Separate your folder paths with a single space to create them all at once
        mkdir -p /opt/airflow/artifacts /opt/airflow/data /opt/airflow/models /opt/airflow/outputs
        
        # Grant permissions to all of them together
        chmod 777 /opt/airflow/artifacts /opt/airflow/data /opt/airflow/models /opt/airflow/outputs
        
        exec /entrypoint version
```