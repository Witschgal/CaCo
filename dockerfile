FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY main.py .

# Create non-root user for security
RUN useradd -m -u 1001 botuser
RUN chown -R botuser:botuser /app
USER botuser

# Expose port for health checks
EXPOSE 3000

# Start the bot
CMD ["python", "main.py"]
