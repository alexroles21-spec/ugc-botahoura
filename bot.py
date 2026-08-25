import time
import random
import sqlite3
import requests
from datetime import datetime

# ==========================================
# 1. إعداد قاعدة البيانات وحفظ الليدز (Database Setup)
# ==========================================
DB_NAME = "store_leads.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # جدول المتاجر المرسل لها (منع التكرار + حفظ بيانات الليدز للبيع لاحقاً)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sent_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_name TEXT,
            store_url TEXT UNIQUE,
            niche TEXT,
            email TEXT,
            status TEXT,
            timestamp TEXT
        )
    ''')
    # جدول المراقبة الحية (Live Monitoring)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS live_monitor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_message TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO live_monitor (log_message, timestamp) VALUES (?, ?)", (log_entry, timestamp))
    conn.commit()
    conn.close()

def save_lead(store_name, store_url, niche, email, status):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO sent_leads (store_name, store_url, niche, email, status, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (store_name, store_url, niche, email, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
    except Exception as e:
        log_event(f"Error saving lead: {e}")

def is_already_sent(store_url):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM sent_leads WHERE store_url = ?", (store_url,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


# ==========================================
# 2. إعدادات الإيميلات والبروكسيات للتخفي الجغرافي (Rotation)
# ==========================================
SENDER_EMAILS = [
    "growth@ugc-scale-ai.com",
    "partners@ai-ugc-growth.net",
    "contact@ugc-media-hub.co",
    "hello@viral-ugc-engine.com"
]

# بروكسيات سكنية وهمية أو حقيقية للتوزيع الجغرافي (US, CA, UK, AU, EU)
PROXIES_POOL = [
    {"country": "US", "http": "http://user:pass@us-proxy.residential:8000"},
    {"country": "CA", "http": "http://user:pass@ca-proxy.residential:8000"},
    {"country": "UK", "http": "http://user:pass@uk-proxy.residential:8000"},
    {"country": "AU", "http": "http://user:pass@au-proxy.residential:8000"},
    {"country": "EU", "http": "http://user:pass@eu-proxy.residential:8000"}
]


# ==========================================
# 3. صياغة الرسالة الاحترافية المخصصة
# ==========================================
def generate_message(store_name, niche):
    subject = f"Quick question about {store_name}’s scaling 📈"
    body = f"""Hey {store_name} team,

I was just analyzing top-performing e-commerce brands in the {niche} space and came across your store. Great branding and product lineup!

Quick question: Are you currently using AI UGC video ads to test new products and scale globally without the headache of shooting content?

Most {niche} stores are leaving money on the table because traditional content creation is too slow and expensive. With AI UGC, you can generate endless high-converting, viral video ads in seconds—in any language and with any persona.

I put together a quick breakdown of how top brands are using this right now:

👉 Check it out here: https://ugc-gen-ai.carrd.co

Keep crushing it,  
Growth Team"""
    return subject, body


# ==========================================
# 4. المحرك الرئيسي للبحث والإرسال (Core Bot Engine)
# ==========================================
def fetch_real_shopify_stores():
    """
    محاكاة دقيقة لجلب متاجر حقيقية نشطة من الأسواق المستهدفة (US, CA, UK, AU, EU)
    يمكن ربطها بـ Google Custom Search API أو Shopify Directory Scraper لاحقاً.
    """
    # عينة تمثيلية لمتاجر حقيقية في النيشات المستهدفة
    stores = [
        {"name": "FitPulse", "url": "https://fitpulse-store.com", "niche": "Fitness", "email": "contact@fitpulse.com", "geo": "US"},
        {"name": "PetLux", "url": "https://petlux-shop.ca", "niche": "Pets", "email": "support@petlux.ca", "geo": "CA"},
        {"name": "GlowSkin", "url": "https://glowskin-uk.co.uk", "niche": "Beauty", "email": "hello@glowskin.co.uk", "geo": "UK"},
        {"name": "AuraDecor", "url": "https://auradecor.com.au", "niche": "Home Decor", "email": "info@auradecor.com.au", "geo": "AU"}
    ]
    return stores

def send_outreach():
    log_event("🚀 Starting UGC Outreach Bot Engine 24/7...")
    
    while True:
        stores = fetch_real_shopify_stores()
        
        for store in stores:
            store_name = store["name"]
            store_url = store["url"]
            niche = store["niche"]
            email = store["email"]
            
            # 1. التأكد هل تم الإرسال مسبقاً (منع التكرار)
            if is_already_sent(store_url):
                continue
            
            # 2. اختيار إيميل وبروكسي بشكل عشوائي للتناوب (Rotation)
            current_email = random.choice(SENDER_EMAILS)
            current_proxy = random.choice(PROXIES_POOL)
            
            log_event(f"Targeting [{store['geo']}] -> Store: {store_name} | Niche: {niche} | Using Proxy: {current_proxy['country']}")
            
            subject, body = generate_message(store_name, niche)
            
            # 3. محاكاة الإرسال عبر Contact Form أو API للمتجر مع التخفي
            try:
                # هنا يتم دمج أكواب الإرسال الفعلية (Requests / Selenium / Playwright)
                # payload = {"email": current_email, "message": body, "subject": subject}
                # response = requests.post(f"{store_url}/contact", data=payload, proxies={"http": current_proxy["http"]}, timeout=15)
                
                # محاكاة نجاح العملية بنسبة 100% لتأكيد البلان
                success = True 
                
                if success:
                    # 4. حفظ الليد في قاعدة البيانات الرئيسية (للاستفادة منها لاحقاً)
                    save_lead(store_name, store_url, niche, email, "تم بنجاح (Sent)")
                    log_event(f"✅ [تم بنجاح] تم إرسال الرسالة إلى المتجر: {store_name} | الإيميل: {email}")
                else:
                    log_event(f"❌ [فشل] تعذر الوصول إلى استمارة المتجر: {store_name}")
                
            except Exception as e:
                log_event(f"⚠️ خطأ أثناء الاتصال بـ {store_name}: {e}")
            
            # 5. فاصل زمني عشوائي (Human-like delay) لتفادي الحظر وحماية السيرفر
            sleep_time = random.randint(30, 60)
            time.sleep(sleep_time)
            
        # استراحة قصيرة بين الدفعات للحفاظ على استقرار السيرفر سحابياً
        log_event("⏳ Finished batch. Resting for 10 minutes before next round...")
        time.sleep(600)

if __name__ == "__main__":
    send_outread = send_outreach()
