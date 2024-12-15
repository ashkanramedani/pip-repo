# Dockerfile

# استفاده از تصویر رسمی پایتون
FROM python:3.11.4

# تنظیم متغیر محیطی برای جلوگیری از ایجاد فایل‌های pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ایجاد پوشه کاری
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# تنظیم pip با استفاده از pip.conf
COPY ./pip.conf /etc/pip.conf

# نصب pip و وابستگی‌ها
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ایجاد پوشه لاگ‌ها
RUN mkdir -p logs

# Copy app files
COPY . .

# باز کردن پورت مورد نیاز
EXPOSE 5000

CMD ["python", "-m", "http.server", "5000"]
