build:
	docker build -t fastapi_example .
run:
	docker run -p 8000:8000 fastapi_example

db-shell:
	psql -h localhost -U postgres -d postgres -W

