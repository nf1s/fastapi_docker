install:
	pipenv install

run-local:
	pipenv run python main.py

build:
	docker build -t fastapi_example .

run:
	docker run --rm --name app --net=mynet -p 8000:8000 fastapi_example

postgres-start:
	docker run \
		--rm   \
		--name  postgres \
		--net=mynet \
		-p 5432:5432 \
		-e POSTGRES_USER=postgres \
		-e POSTGRES_PASSWORD=postgres \
		-e POSTGRES_DB=postgres \
		-d postgres

postgres-stop:
	docker stop postgres

db-shell:
	psql -h localhost -U postgres -d postgres -W

