from flask import Flask, render_template_string, send_from_directory, jsonify
import os
import logging
from subprocess import run

app = Flask(__name__)

# مسیر دایرکتوری مخزن محلی
repo_path = "/usr/src/app/packages"

# تنظیمات لاگ برای اشکال‌زدایی
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/simple/')
def list_packages():
    """لیست تمامی بسته‌ها در دایرکتوری مخزن."""
    try:
        # لیست دایرکتوری‌های موجود
        packages = [p for p in os.listdir(repo_path) if os.path.isdir(os.path.join(repo_path, p))]
        links = [f'<a href="{p}/">{p}</a>' for p in packages]
        template = '''
        <!doctype html>
        <html>
          <head><title>Simple Index</title></head>
          <body>
            {{ links|safe }}
          </body>
        </html>
        '''
        return render_template_string(template, links='<br>'.join(links))
    except Exception as e:
        logger.error(f"Error listing packages: {e}")
        return jsonify({"error": "Failed to list packages"}), 500

@app.route('/simple/<package_name>/')
def list_package_versions(package_name):
    """لیست نسخه‌های موجود برای یک بسته خاص."""
    package_dir = os.path.join(repo_path, package_name)
    if not os.path.exists(package_dir):
        os.makedirs(package_dir, exist_ok=True)
        # تلاش برای دانلود از PyPI
        result = run(
            ["pip", "download", package_name, "-d", package_dir],
            capture_output=True,
            text=True
        )
        logger.debug(f"pip download stdout: {result.stdout}")
        logger.debug(f"pip download stderr: {result.stderr}")
        if result.returncode != 0:
            logger.error(f"Failed to download {package_name}: {result.stderr}")
            return jsonify({
                "error": f"Package '{package_name}' not found on PyPI",
                "details": result.stderr
            }), 404

    # فهرست فایل‌های موجود در دایرکتوری بسته
    try:
        files = [f'<a href="{f}">{f}</a>' for f in os.listdir(package_dir)]
        template = '''
        <!doctype html>
        <html>
          <head><title>{{ package_name }} - Versions</title></head>
          <body>
            {{ files|safe }}
          </body>
        </html>
        '''
        return render_template_string(template, package_name=package_name, files='<br>'.join(files))
    except Exception as e:
        logger.error(f"Error listing versions for {package_name}: {e}")
        return jsonify({"error": "Failed to list package versions"}), 500

@app.route('/simple/<package_name>/<filename>', methods=['GET'])
def download_file(package_name, filename):
    """دانلود یک فایل خاص از مسیر بسته."""
    package_dir = os.path.join(repo_path, package_name)
    try:
        # بازگرداندن فایل از دایرکتوری مربوط به بسته
        return send_from_directory(package_dir, filename)
    except Exception as e:
        logger.error(f"Error serving file {filename}: {e}")
        return jsonify({"error": f"File '{filename}' not found"}), 404

if __name__ == '__main__':
    # اجرای برنامه Flask
    app.run(host='0.0.0.0', port=5000)
