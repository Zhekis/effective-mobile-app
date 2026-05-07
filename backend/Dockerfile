FROM python:3.12-slim AS builder

WORKDIR /app
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser

FROM python:3.12-slim

COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group

WORKDIR /app

COPY --chown=appuser:appgroup app.py .

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/')" || exit 1

CMD ["python", "-u", "app.py"]
