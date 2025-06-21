.PHONY: es-up es-down es-clean qdrant-up qdrant-down qdrant-clean up down clean

# ElasticSearch
es-up:
	docker compose -f docker/elasticsearch/docker-compose.yml up -d

es-down:
	docker compose -f docker/elasticsearch/docker-compose.yml down

es-clean:
	docker compose -f docker/elasticsearch/docker-compose.yml down -v

# Qdrant
qdrant-up:
	docker compose -f docker/qdrant/docker-compose.yml up -d

qdrant-down:
	docker compose -f docker/qdrant/docker-compose.yml down

qdrant-clean:
	docker compose -f docker/qdrant/docker-compose.yml down -v

up: es-up qdrant-up

down: es-down qdrant-down

clean: es-clean qdrant-clean

