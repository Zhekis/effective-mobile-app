```markdown
# Effective Mobile - Веб-приложение на Docker

Простое веб-приложение с reverse-proxy на Nginx, полностью контейнеризированное с помощью Docker Compose.

## Архитектура

```
Пользователь -> HTTP :80 -> Nginx (reverse proxy) -> Backend (Python) :8080 -> Ответ
                                      |
                                      +----> Проксирование заголовков (Host, X-Real-IP и др.)
```

**Компоненты:**
- **Nginx** (порт 80) - Reverse proxy, принимает все входящие запросы
- **Backend** (порт 8080) - Python HTTP сервер, недоступен извне, только через Nginx
- **Docker Network** - Изолированная сеть для взаимодействия контейнеров

## Технологии

- Docker & Docker Compose v3.8
- Nginx 1.26 (Alpine Linux)
- Python 3.12 (Slim)
- Alpine Linux base images

## Требования

- Docker Engine 20.10+
- Docker Compose 2.0+

## Быстрый запуск

```bash
# Клонировать репозиторий
git clone https://github.com/Zhekis/effective-mobile-app.git
cd effective-mobile-app

# Запустить контейнеры
docker-compose up -d

# Проверить статус
docker-compose ps

# Проверить работу
curl http://localhost
```

## Проверка работоспособности

### Через curl
```bash
$ curl http://localhost
Hello from Effective Mobile!
```

### Через браузер
Открыть `http://localhost`

### Проверка healthcheck'ов
```bash
# Статус контейнеров
docker ps

# Логи backend
docker logs effective-mobile-backend

# Логи nginx
docker logs effective-mobile-nginx
```

## Структура проекта

```
effective-mobile-app/
├── backend/
│   ├── Dockerfile      # Многостадийная сборка, non-root user
│   └── app.py          # Python HTTP сервер с поддержкой GET/HEAD
├── nginx/
│   └── nginx.conf      # Конфигурация reverse-proxy с upstream
├── docker-compose.yml  # Оркестрация с изолированной сетью
├── .gitignore          # Исключения для Git
├── LICENSE             # MIT лицензия
└── README.md           # Документация
```

## Детали реализации

### Backend (Python)
- **Файл:** `backend/app.py`
- **Порт:** 8080 (только внутри Docker сети)
- **Endpoint:** `/` - возвращает `"Hello from Effective Mobile!"`
- **Поддерживаемые методы:** GET, HEAD (для healthcheck)
- **Запуск:** От non-root пользователя (UID 1001)
- **Healthcheck:** Каждые 30 секунд проверяет доступность эндпоинта

### Nginx (Reverse Proxy)
- **Файл конфигурации:** `nginx/nginx.conf`
- **Порт на хосте:** 80
- **Upstream:** `backend:8080` (по имени сервиса)
- **Проксирование заголовков:** Host, X-Real-IP, X-Forwarded-For
- **Keepalive соединения:** 32 соединения
- **Отключено:** Буферизация, server tokens
- **Таймауты:** Защита от медленных атак
- **Healthcheck:** Каждые 30 секунд через wget

### Docker Compose
- **Сеть:** `effective-mobile-network` (изолированная bridge сеть)
- **Зависимости:** Nginx запускается только после healthy статуса backend
- **Перезапуск:** `unless-stopped` - автоматический перезапуск при ошибках
- **Healthcheck:** Для обоих сервисов

## Безопасность

### Реализованные меры

| Мера | Реализация |
|------|------------|
| Non-root пользователь | Запуск backend от UID 1001 |
| Изоляция портов | Backend имеет только expose, нет ports |
| Отключение server tokens | `server_tokens off` в nginx |
| Таймауты запросов | Защита от медленных атак |
| Минимальные образы | `python:3.12-slim`, `nginx:1.26-alpine` |
| Healthcheck'и | Мониторинг состояния сервисов |

### Проверка безопасности

```bash
# Проверка, что backend не доступен с хоста
curl http://localhost:8080  # Должен быть Connection refused

# Проверка пользователя в контейнере
docker exec effective-mobile-backend whoami  # Вывод: appuser

# Проверка что nginx не выдает версию
curl -I http://localhost | grep Server  # Вывод отсутствует
```

## Диагностика

### Просмотр логов

```bash
# Логи всех сервисов
docker-compose logs

# Логи конкретного сервиса
docker-compose logs backend
docker-compose logs nginx

# Логи в реальном времени
docker-compose logs -f
```

### Сетевая диагностика

```bash
# Просмотр сети Docker
docker network inspect effective-mobile-network

# Проверка связи между контейнерами
docker exec effective-mobile-nginx ping -c 2 backend

# Проверка доступа к backend из nginx
docker exec effective-mobile-nginx wget -qO- http://backend:8080
```

## Устранение неполадок

### Проблема: Порт 80 уже занят

**Решение:**
```bash
# Изменить порт в docker-compose.yml
sed -i 's/"80:80"/"8080:80"/g' docker-compose.yml
docker-compose up -d
curl http://localhost:8080
```

### Проблема: Контейнеры не запускаются

**Решение:**
```bash
# Пересобрать и запустить заново
docker-compose down
docker-compose up -d --build

# Проверить логи
docker-compose logs
```

## Результат работы

```bash
$ curl http://localhost
Hello from Effective Mobile!

$ docker ps --format "table {{.Names}}\t{{.Status}}"
NAMES                      STATUS
effective-mobile-nginx     Up (healthy)
effective-mobile-backend   Up (healthy)
```

## Лицензия

MIT License - подробнее в файле [LICENSE](LICENSE)
