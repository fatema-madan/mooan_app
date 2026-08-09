import streamlit as st
from datetime import date, timedelta
import math
from pathlib import Path
import os
import json
import base64
from io import BytesIO

LOGO_PATH = "assets/logo.png" if Path("assets/logo.png").exists() else ("logo.png" if Path("logo.png").exists() else None)

st.set_page_config(page_title="MOOAN | مؤن", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

PRIMARY = "#123D2A"
ACCENT = "#78A83B"
GOLD = "#E4A82B"
RED = "#C84A3A"
BG = "#F7F8F3"

st.markdown(f"""
<style>
.stApp {{background:{BG};}}
section[data-testid="stSidebar"] {{background:{PRIMARY};}}
section[data-testid="stSidebar"] * {{color:white !important;}}
div[data-testid="stMetric"] {{background:white;border:1px solid #e5e8df;border-radius:16px;padding:14px;}}
.stButton>button {{background:{PRIMARY};color:white;border:0;border-radius:12px;font-weight:650;}}
.stButton>button:hover {{background:{ACCENT};color:white;}}
.mooan-card {{background:white;border:1px solid #e5e8df;border-radius:18px;padding:18px;margin-bottom:10px;}}
.mooan-soft {{background:#eef4e8;border-radius:18px;padding:18px;}}
.mooan-badge {{display:inline-block;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:700;color:white;}}
.login-wrap {{max-width:620px;margin:4rem auto 1rem auto;}}
h1,h2,h3 {{color:{PRIMARY};}}
</style>
""", unsafe_allow_html=True)

T = {
"en": {
"welcome":"Welcome to MOOAN","tag":"Fresh food. Smarter kitchen. Less waste.",
"login":"Log in","signup":"Create account","email":"Email","password":"Password","name":"Full name",
"household":"Household","business":"Business","account_type":"Account type","enter":"Enter MOOAN",
"demo":"Demo: enter any email and password.","nav":"Navigate","home":"Home","market":"Marketplace",
"stores":"Nearby Stores","pantry":"My Pantry","scan":"AI Scan","recipes":"Smart Recipes","rewards":"Rewards","profile":"Profile",
"logout":"Log out","hello":"Good to see you","impact":"Your food impact this month","saved_food":"Used before expiry",
"expired":"Expired / unused","save_rate":"Food saved rate","points":"MOOAN Points","shop":"Fresh picks",
"add":"Add to cart","cart":"Cart","checkout":"Checkout","empty":"Your cart is empty.",
"area":"Choose your area","mapnote":"Showing real store locations from the built-in Bahrain MVP dataset. Distance is shown only when a reference location is available.",
"items":"Pantry items","use":"I used it","discard":"Expired / discarded","days":"days left","today":"Expires today",
"add_item":"Add pantry item","quantity":"Quantity (kg)","expiry_date":"Expiry date","freshness":"Freshness",
"recipe_title":"Recipes prioritized by freshness & expiry","calories":"kcal","make":"I made this recipe",
"reward_title":"Use food before expiry. Earn rewards.","redeem":"Redeem","scan_note":"MVP simulation: upload a produce photo to record a freshness check. A production version would use a trained computer-vision model.",
"profile_sub":"Your MOOAN account and impact summary","language":"Language","verified":"MOOAN Verified",
"used_reward":"Great! Food saved and points added.","discarded_msg":"Item recorded as expired/unused.","reward_ok":"Reward redeemed!","need_points":"You need more points.",
},
"ar": {
"welcome":"أهلاً بك في مؤن","tag":"غذاء طازج. مطبخ أذكى. هدر أقل.",
"login":"تسجيل الدخول","signup":"إنشاء حساب","email":"البريد الإلكتروني","password":"كلمة المرور","name":"الاسم الكامل",
"household":"منزل","business":"نشاط تجاري","account_type":"نوع الحساب","enter":"دخول مؤن",
"demo":"نسخة تجريبية: أدخل أي بريد وكلمة مرور.","nav":"التنقل","home":"الرئيسية","market":"السوق",
"stores":"المتاجر القريبة","pantry":"مؤنتي","scan":"فحص الذكاء الاصطناعي","recipes":"الوصفات الذكية","rewards":"المكافآت","profile":"الملف الشخصي",
"logout":"تسجيل الخروج","hello":"سعدنا بعودتك","impact":"أثر استخدامك للطعام هذا الشهر","saved_food":"استخدم قبل انتهاء الصلاحية",
"expired":"منتهي / غير مستخدم","save_rate":"معدل الاستفادة من الطعام","points":"نقاط مؤن","shop":"مختارات طازجة",
"add":"أضف للسلة","cart":"السلة","checkout":"إتمام الطلب","empty":"سلتك فارغة.",
"area":"اختر منطقتك","mapnote":"نعرض مواقع متاجر حقيقية من بيانات MVP المحفوظة للبحرين. لا نعرض المسافة إلا عند توفر موقع مرجعي.",
"items":"محتويات المؤن","use":"استخدمته","discard":"انتهى / تم التخلص منه","days":"أيام متبقية","today":"ينتهي اليوم",
"add_item":"إضافة منتج للمؤن","quantity":"الكمية (كجم)","expiry_date":"تاريخ الانتهاء","freshness":"النضارة",
"recipe_title":"وصفات مرتبة حسب النضارة وقرب انتهاء الصلاحية","calories":"سعرة","make":"حضّرت هذه الوصفة",
"reward_title":"استخدم الطعام قبل انتهاء صلاحيته واجمع المكافآت.","redeem":"استبدال","scan_note":"محاكاة MVP: ارفع صورة منتج لتسجيل فحص النضارة. النسخة الفعلية ستستخدم نموذج رؤية حاسوبية مدرب.",
"profile_sub":"حسابك وملخص أثرك في مؤن","language":"اللغة","verified":"موثّق من مؤن",
"used_reward":"رائع! تم تسجيل الطعام المستخدم وإضافة النقاط.","discarded_msg":"تم تسجيل المنتج كمنتهي/غير مستخدم.","reward_ok":"تم استبدال المكافأة!","need_points":"تحتاج نقاط أكثر.",
}}

PRODUCTS = [
{"id":1,"en":"Red Apples","ar":"تفاح أحمر","cat":"Fruits","price":0.850,"unit":"1 kg","emoji":"🍎","supplier":"Green Valley Farm"},
{"id":2,"en":"Bananas","ar":"موز","cat":"Fruits","price":0.600,"unit":"1 kg","emoji":"🍌","supplier":"Sunny Farms"},
{"id":3,"en":"Strawberries","ar":"فراولة","cat":"Fruits","price":0.950,"unit":"250 g","emoji":"🍓","supplier":"Green Valley Farm"},
{"id":4,"en":"Tomatoes","ar":"طماطم","cat":"Vegetables","price":0.500,"unit":"1 kg","emoji":"🍅","supplier":"Bahrain Organics"},
{"id":5,"en":"Carrots","ar":"جزر","cat":"Vegetables","price":0.400,"unit":"1 kg","emoji":"🥕","supplier":"Bahrain Organics"},
{"id":6,"en":"Leafy Greens","ar":"خضار ورقية","cat":"Vegetables","price":0.700,"unit":"300 g","emoji":"🥬","supplier":"Green Valley Farm"},
]

# Publicly recognizable Bahrain locations are used as an MVP reference dataset.
STORES = [
{"name":"Carrefour - Bahrain City Centre","area":"Manama","lat":26.2325,"lon":50.5535,"verified":True},
{"name":"Lulu Hypermarket - Dana Mall","area":"Manama","lat":26.2300,"lon":50.5480,"verified":False},
{"name":"Alosra Supermarket - Amwaj","area":"Muharraq","lat":26.2860,"lon":50.6650,"verified":True},
{"name":"Lulu Hypermarket - Hidd","area":"Muharraq","lat":26.2150,"lon":50.6540,"verified":False},
{"name":"Lulu Hypermarket - Riffa","area":"Riffa","lat":26.1290,"lon":50.5550,"verified":True},
{"name":"Al Jazira Supermarket - Zinj","area":"Manama","lat":26.2070,"lon":50.5650,"verified":True},
]
AREA_CENTER = {
"Manama":(26.2235,50.5876),
"Muharraq":(26.2572,50.6119),
"Riffa":(26.1300,50.5550),
}

RECIPES = [
{"en":"Use-Soon Tomato Pasta","ar":"باستا الطماطم للاستخدام السريع","uses":["Tomatoes"],"kcal":410,"time":25,"emoji":"🍝"},
{"en":"Ripe Banana Oat Pancakes","ar":"بانكيك الشوفان بالموز الناضج","uses":["Bananas"],"kcal":330,"time":15,"emoji":"🥞"},
{"en":"Strawberry Yogurt Bowl","ar":"وعاء الفراولة والزبادي","uses":["Strawberries"],"kcal":240,"time":10,"emoji":"🍓"},
{"en":"Roasted Carrot Salad","ar":"سلطة الجزر المشوي","uses":["Carrots","Leafy Greens"],"kcal":290,"time":30,"emoji":"🥗"},
]

if "lang" not in st.session_state: st.session_state.lang = "en"
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user" not in st.session_state: st.session_state.user = {"name":"MOOAN User","email":""}
if "cart" not in st.session_state: st.session_state.cart = {}
if "points" not in st.session_state: st.session_state.points = 120
if "food_used_kg" not in st.session_state: st.session_state.food_used_kg = 1.25
if "food_expired_kg" not in st.session_state: st.session_state.food_expired_kg = 0.20
if "pantry" not in st.session_state:
    today=date.today()
    st.session_state.pantry=[
        {"name":"Strawberries","ar":"فراولة","emoji":"🍓","qty":0.25,"expiry":today+timedelta(days=1),"freshness":68,"price_per_kg":3.8},
        {"name":"Tomatoes","ar":"طماطم","emoji":"🍅","qty":0.60,"expiry":today+timedelta(days=2),"freshness":74,"price_per_kg":0.5},
        {"name":"Red Apples","ar":"تفاح أحمر","emoji":"🍎","qty":1.00,"expiry":today+timedelta(days=8),"freshness":94,"price_per_kg":0.85},
        {"name":"Carrots","ar":"جزر","emoji":"🥕","qty":0.75,"expiry":today+timedelta(days=10),"freshness":96,"price_per_kg":0.4},
    ]

def tr(k): return T[st.session_state.lang][k]
def pname(p): return p["ar"] if st.session_state.lang=="ar" else p["en"]
def item_name(i): return i.get("ar",i["name"]) if st.session_state.lang=="ar" else i["name"]
def saved_rate():
    total=st.session_state.food_used_kg+st.session_state.food_expired_kg
    return (st.session_state.food_used_kg/total*100) if total else 0

def expiring_items(days_threshold=2):
    today = date.today()
    return [
        item for item in st.session_state.pantry
        if 0 <= (item["expiry"] - today).days <= days_threshold
    ]

def expired_items():
    today = date.today()
    return [
        item for item in st.session_state.pantry
        if (item["expiry"] - today).days < 0
    ]
def cart_total():
    return sum(next(p["price"] for p in PRODUCTS if p["id"]==pid)*qty for pid,qty in st.session_state.cart.items())
def urgency(item):
    d=(item["expiry"]-date.today()).days
    return (d, item["freshness"])
def points_for(item):
    d=(item["expiry"]-date.today()).days
    # More points for preventing imminent waste; quantity keeps reward proportional.
    multiplier=2 if d<=1 else (1.5 if d<=3 else 1)
    return max(5, round(item["qty"]*20*multiplier))
def use_item(index):
    item=st.session_state.pantry[index]
    st.session_state.food_used_kg += item["qty"]
    st.session_state.points += points_for(item)
    del st.session_state.pantry[index]
def discard_item(index):
    item=st.session_state.pantry[index]
    st.session_state.food_expired_kg += item["qty"]
    del st.session_state.pantry[index]


def _get_openai_key():
    """Read API key safely from Streamlit secrets or environment."""
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    return os.getenv("OPENAI_API_KEY")

def analyze_food_image(image_file, mode):
    """
    Real AI analysis when OPENAI_API_KEY is configured.
    mode = 'expiry' for packaged food/date reading
           'freshness' for fruit/vegetable ripeness
    """
    api_key = _get_openai_key()
    if not api_key:
        return None, "NO_API_KEY"

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        raw = image_file.getvalue()
        mime = getattr(image_file, "type", None) or "image/jpeg"
        encoded = base64.b64encode(raw).decode("utf-8")
        data_url = f"data:{mime};base64,{encoded}"

        if mode == "expiry":
            prompt = """
You are the vision component of a food-management app called MOOAN.
Inspect the package image carefully and read any printed expiry/best-before/use-by date.
Return ONLY valid JSON with these fields:
{
  "product_name": string or null,
  "expiry_text": string or null,
  "expiry_date_iso": "YYYY-MM-DD" or null,
  "date_type": "expiry" | "best_before" | "use_by" | "unknown",
  "confidence": integer 0-100,
  "note": short string
}
Important:
- Do not invent a date. If the date is unreadable or ambiguous, return null.
- If multiple dates exist, choose the one most likely to be expiry/best-before/use-by and explain briefly in note.
"""
        else:
            prompt = """
You are the vision component of a food-management app called MOOAN.
Inspect the image of fruit or vegetables and estimate visible ripeness/freshness from appearance only.
Return ONLY valid JSON with these fields:
{
  "product_name": string or null,
  "category": "fruit" | "vegetable" | "other",
  "ripeness_level": "unripe" | "ripe" | "very_ripe" | "overripe" | "spoiled" | "unknown",
  "freshness_score": integer 0-100 or null,
  "recommended_action": "wait" | "use_now" | "use_soon" | "discard" | "unknown",
  "confidence": integer 0-100,
  "note": short string
}
Important:
- This is a visual estimate, not a food-safety diagnosis.
- Do not claim safety from appearance alone.
- If image quality is poor or the item cannot be identified, use unknown/null.
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": data_url},
                ],
            }],
        )
        out = response.output_text.strip()
        # Remove accidental code fences if present
        out = re.sub(r"^```(?:json)?\s*|\s*```$", "", out, flags=re.S)
        return json.loads(out), None
    except Exception as e:
        return None, str(e)


# Language control is available before login.
top1, top2 = st.columns([5,1])
with top2:
    lang_label=st.selectbox("🌐",["English","العربية"],index=0 if st.session_state.lang=="en" else 1,label_visibility="collapsed")
    st.session_state.lang="ar" if lang_label=="العربية" else "en"

if not st.session_state.logged_in:
    st.markdown("<div class='login-wrap'>",unsafe_allow_html=True)
    if LOGO_PATH:
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            st.image(LOGO_PATH, use_container_width=True)
    else:
        st.markdown("<div style='text-align:center;font-size:72px'>🌿</div>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center'>{tr('welcome')}</h1><p style='text-align:center;color:#687269'>{tr('tag')}</p>",unsafe_allow_html=True)
    tab1,tab2=st.tabs([tr("login"),tr("signup")])
    with tab1:
        email=st.text_input(tr("email"),key="login_email")
        password=st.text_input(tr("password"),type="password",key="login_pw")
        st.caption(tr("demo"))
        if st.button(tr("enter"),use_container_width=True,key="login_btn"):
            if email and password:
                st.session_state.user={"name":email.split("@")[0].title(),"email":email}
                st.session_state.logged_in=True
                st.rerun()
            else: st.warning("Please enter email and password." if st.session_state.lang=="en" else "أدخل البريد وكلمة المرور.")
    with tab2:
        nm=st.text_input(tr("name"),key="signup_name")
        em=st.text_input(tr("email"),key="signup_email")
        pw=st.text_input(tr("password"),type="password",key="signup_pw")
        st.selectbox(tr("account_type"),[tr("household"),tr("business")])
        if st.button(tr("signup"),use_container_width=True,key="signup_btn"):
            if nm and em and pw:
                st.session_state.user={"name":nm,"email":em}
                st.session_state.logged_in=True
                st.rerun()
            else: st.warning("Complete all fields." if st.session_state.lang=="en" else "أكمل جميع الحقول.")
    st.markdown("</div>",unsafe_allow_html=True)
    st.stop()

with st.sidebar:
    if LOGO_PATH:
        st.image(LOGO_PATH, width=120)
    else:
        st.markdown("<div style='text-align:center;font-size:48px'>🌿</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;color:white'>MOOAN | مؤن</h2>",unsafe_allow_html=True)
    st.caption(st.session_state.user["name"])
    labels=[tr("home"),tr("market"),tr("stores"),tr("pantry"),tr("scan"),tr("recipes"),tr("rewards"),tr("profile")]
    icons=["🏠","🛒","📍","📦","📷","🍳","🌱","👤"]
    page=st.radio(tr("nav"),[f"{i} {l}" for i,l in zip(icons,labels)],label_visibility="collapsed")
    st.divider()
    st.write(f"🛍️ {tr('cart')}: **{sum(st.session_state.cart.values())}**")
    st.write(f"🌱 {tr('points')}: **{st.session_state.points}**")
    soon_count = len(expiring_items(2))
    if soon_count:
        st.warning(
            f"⏰ {soon_count} item(s) expiring soon"
            if st.session_state.lang=="en"
            else f"⏰ {soon_count} منتج قريب انتهاء صلاحيته"
        )
    if st.button(tr("logout"),use_container_width=True):
        st.session_state.logged_in=False
        st.rerun()

page_idx=[f"{i} {l}" for i,l in zip(icons,labels)].index(page)

if page_idx==0:
    st.title(f"{tr('hello')}, {st.session_state.user['name']} 👋")
    st.write(tr("tag"))

    soon = expiring_items(2)
    overdue = expired_items()

    if overdue:
        names = ", ".join(item_name(i) for i in overdue[:3])
        st.error(
            f"🚨 Expired items detected: {names}. Review your pantry."
            if st.session_state.lang=="en"
            else f"🚨 توجد منتجات منتهية: {names}. راجعي المؤن."
        )

    if soon:
        soon_sorted = sorted(soon, key=lambda x: x["expiry"])
        names = ", ".join(item_name(i) for i in soon_sorted[:3])
        st.warning(
            f"⏰ Use soon: {names}. These items expire within 2 days."
            if st.session_state.lang=="en"
            else f"⏰ استخدمي قريباً: {names}. هذه المنتجات تنتهي خلال يومين."
        )

        notif_key = "|".join(f"{i['name']}:{i['expiry']}" for i in soon_sorted)
        if st.session_state.get("last_expiry_notice") != notif_key:
            st.toast(
                "You have food expiring soon 🍓"
                if st.session_state.lang=="en"
                else "عندك أطعمة قريبة انتهاء الصلاحية 🍓"
            )
            st.session_state["last_expiry_notice"] = notif_key
    a,b,c,d=st.columns(4)
    a.metric("♻️ "+tr("saved_food"),f"{st.session_state.food_used_kg:.2f} kg")
    b.metric("🗑️ "+tr("expired"),f"{st.session_state.food_expired_kg:.2f} kg")
    c.metric("🌿 "+tr("save_rate"),f"{saved_rate():.1f}%")
    d.metric("⭐ "+tr("points"),st.session_state.points)
    st.caption(("Food saved rate = food recorded as used before expiry ÷ (used before expiry + expired/unused). It is an in-app utilization metric, not a claim of causal waste reduction."
                if st.session_state.lang=="en" else
                "معدل الاستفادة = الطعام المسجل كمستخدم قبل انتهاء الصلاحية ÷ (المستخدم قبل الانتهاء + المنتهي/غير المستخدم). وهو مقياس استخدام داخل التطبيق وليس ادعاءً بأن مؤن تسبب وحدها في خفض الهدر."))
    st.subheader("⚠️ "+("Use soon" if st.session_state.lang=="en" else "استخدم قريباً"))
    for item in sorted(st.session_state.pantry,key=urgency)[:3]:
        days=(item["expiry"]-date.today()).days
        st.markdown(f"<div class='mooan-card'>{item['emoji']} <b>{item_name(item)}</b> · {item['qty']:.2f} kg · {max(days,0)} {tr('days')} · {item['freshness']}% {tr('freshness')}</div>",unsafe_allow_html=True)

elif page_idx==1:
    st.title("🛒 "+tr("market"))
    q=st.text_input("Search" if st.session_state.lang=="en" else "بحث")
    cols=st.columns(3)
    for i,p in enumerate([x for x in PRODUCTS if q.lower() in pname(x).lower()]):
        with cols[i%3]:
            st.markdown(f"<div class='mooan-card'><div style='font-size:42px;text-align:center'>{p['emoji']}</div><b>{pname(p)}</b><br><small>{p['supplier']} · {p['unit']}</small><br><b>BHD {p['price']:.3f}</b></div>",unsafe_allow_html=True)
            if st.button("➕ "+tr("add"),key=f"add{p['id']}"):
                st.session_state.cart[p["id"]]=st.session_state.cart.get(p["id"],0)+1
                st.toast(pname(p))
    st.divider(); st.subheader("🛍️ "+tr("cart"))
    if not st.session_state.cart: st.info(tr("empty"))
    else:
        for pid,qty in list(st.session_state.cart.items()):
            p=next(x for x in PRODUCTS if x["id"]==pid)
            c1,c2,c3=st.columns([4,1,1])
            c1.write(f"{p['emoji']} **{pname(p)}** × {qty}")
            c2.write(f"BHD {p['price']*qty:.3f}")
            if c3.button("🗑️",key=f"del{pid}"):
                del st.session_state.cart[pid]; st.rerun()
        st.markdown(f"### Total: BHD {cart_total():.3f}")
        if st.button("✅ "+tr("checkout")):
            # Purchased fresh items enter the digital pantry automatically in this MVP.
            for pid,qty in st.session_state.cart.items():
                p=next(x for x in PRODUCTS if x["id"]==pid)
                kg=qty*(0.25 if "250" in p["unit"] else 0.3 if "300" in p["unit"] else 1.0)
                st.session_state.pantry.append({"name":p["en"],"ar":p["ar"],"emoji":p["emoji"],"qty":kg,
                    "expiry":date.today()+timedelta(days=7),"freshness":95,"price_per_kg":p["price"]/kg if kg else p["price"]})
            st.session_state.cart={}
            st.success("Order placed and items synced to pantry." if st.session_state.lang=="en" else "تم الطلب ومزامنة المنتجات مع المؤن.")
            st.rerun()

elif page_idx==2:
    st.title("📍 "+tr("stores"))
    area=st.selectbox(tr("area"),list(AREA_CENTER.keys()))
    subset=[s for s in STORES if s["area"]==area]
    st.caption(tr("mapnote"))
    if subset:
        import pandas as pd
        df=pd.DataFrame(subset)
        st.map(df,latitude="lat",longitude="lon",size=120)
        for s in subset:
            badge=f" · ✅ {tr('verified')}" if s["verified"] else ""
            st.markdown(f"<div class='mooan-card'><b>{s['name']}</b>{badge}<br><small>{s['area']}, Bahrain</small></div>",unsafe_allow_html=True)
    else: st.info("No stores in the current MVP dataset." if st.session_state.lang=="en" else "لا توجد متاجر في بيانات النسخة التجريبية لهذه المنطقة.")

elif page_idx==3:
    st.title("📦 "+tr("pantry"))
    st.caption(("Track quantity, freshness and expiry. Record what was actually used or expired."
                if st.session_state.lang=="en" else "تابع الكمية والنضارة والصلاحية، وسجل ما تم استخدامه أو انتهت صلاحيته فعلياً."))
    for idx,item in enumerate(list(st.session_state.pantry)):
        days=(item["expiry"]-date.today()).days
        c1,c2,c3,c4=st.columns([4,2,1,1])
        c1.markdown(f"### {item['emoji']} {item_name(item)}")
        c1.caption(f"{item['qty']:.2f} kg · {item['freshness']}% {tr('freshness')}")
        c2.write(tr("today") if days<=0 else f"{days} {tr('days')}")
        if c3.button("✅ "+tr("use"),key=f"use{idx}"):
            pts=points_for(item); use_item(idx); st.toast(f"+{pts} 🌱"); st.rerun()
        if c4.button("🗑️ "+tr("discard"),key=f"discard{idx}"):
            discard_item(idx); st.rerun()
        st.progress(item["freshness"]/100)
    with st.expander("➕ "+tr("add_item")):
        with st.form("pantry_form"):
            nm=st.text_input(tr("name"))
            qty=st.number_input(tr("quantity"),0.05,20.0,0.5,0.05)
            exp=st.date_input(tr("expiry_date"),date.today()+timedelta(days=5))
            fresh=st.slider(tr("freshness"),0,100,90)
            if st.form_submit_button(tr("add_item")) and nm:
                st.session_state.pantry.append({"name":nm,"ar":nm,"emoji":"🥬","qty":qty,"expiry":exp,"freshness":fresh,"price_per_kg":0})
                st.rerun()

elif page_idx==4:
    st.title("📷 "+tr("scan"))

    is_ar = st.session_state.lang == "ar"
    st.write(
        "اختر نوع الفحص: اقرأ تاريخ الانتهاء من العبوة، أو افحص مستوى نضج الفاكهة والخضروات."
        if is_ar else
        "Choose a scan: read the expiry date from packaging, or estimate fruit/vegetable ripeness."
    )

    scan_mode_label = st.radio(
        "نوع الفحص" if is_ar else "Scan type",
        [
            "🏷️ قراءة تاريخ الانتهاء" if is_ar else "🏷️ Expiry date scanner",
            "🥑 فحص النضج والنضارة" if is_ar else "🥑 Ripeness & freshness"
        ],
        horizontal=True
    )
    scan_mode = "expiry" if ("الانتهاء" in scan_mode_label or "Expiry" in scan_mode_label) else "freshness"

    source_tab1, source_tab2 = st.tabs(
        ["📸 الكاميرا", "🖼️ رفع صورة"] if is_ar else ["📸 Camera", "🖼️ Upload image"]
    )

    photo = None
    with source_tab1:
        camera_photo = st.camera_input(
            "صوّر العبوة أو المنتج بوضوح" if is_ar else "Take a clear photo of the package or produce",
            key=f"camera_{scan_mode}"
        )
        if camera_photo:
            photo = camera_photo

    with source_tab2:
        uploaded_photo = st.file_uploader(
            "ارفع صورة من الجهاز" if is_ar else "Upload an image from your device",
            type=["png", "jpg", "jpeg"],
            key=f"upload_{scan_mode}"
        )
        if uploaded_photo and photo is None:
            photo = uploaded_photo

    if photo:
        st.image(photo, caption="الصورة المستخدمة للفحص" if is_ar else "Image used for analysis", use_container_width=True)

        if st.button("✨ تحليل الصورة" if is_ar else "✨ Analyze image", use_container_width=True, key=f"analyze_{scan_mode}"):
            with st.spinner("جاري التحليل..." if is_ar else "Analyzing..."):
                result, err = analyze_food_image(photo, scan_mode)

            if err == "NO_API_KEY":
                st.warning(
                    "الفحص الحقيقي يحتاج OPENAI_API_KEY في Streamlit Secrets. الكاميرا تعمل الآن، لكن قراءة التاريخ وتقدير النضج لن يتم اختلاقهما بدون نموذج فعلي."
                    if is_ar else
                    "Real image analysis needs OPENAI_API_KEY in Streamlit Secrets. The camera works now, but MOOAN will not invent an expiry date or ripeness result without a real model."
                )
            elif err:
                st.error(("تعذر تحليل الصورة: " if is_ar else "Could not analyze image: ") + err)
            elif result:
                st.session_state["last_scan_result"] = result
                st.session_state["last_scan_mode"] = scan_mode

    result = st.session_state.get("last_scan_result")
    result_mode = st.session_state.get("last_scan_mode")

    if result and result_mode == scan_mode:
        st.divider()

        if scan_mode == "expiry":
            st.subheader("🏷️ نتيجة قراءة التاريخ" if is_ar else "🏷️ Expiry scan result")

            product_name = result.get("product_name") or ("منتج غير معروف" if is_ar else "Unknown product")
            expiry_iso = result.get("expiry_date_iso")
            confidence = result.get("confidence", 0)
            expiry_text = result.get("expiry_text") or "—"

            c1, c2, c3 = st.columns(3)
            c1.metric("المنتج" if is_ar else "Product", product_name)
            c2.metric("التاريخ المقروء" if is_ar else "Detected date", expiry_iso or expiry_text)
            c3.metric("الثقة" if is_ar else "Confidence", f"{confidence}%")

            st.caption(result.get("note", ""))

            # Allow user verification before saving; OCR/vision dates can be wrong.
            parsed_default = date.today() + timedelta(days=5)
            if expiry_iso:
                try:
                    parsed_default = date.fromisoformat(expiry_iso)
                except Exception:
                    pass

            with st.form("save_expiry_scan"):
                verified_name = st.text_input(
                    "اسم المنتج" if is_ar else "Product name",
                    value=product_name
                )
                verified_expiry = st.date_input(
                    "تأكد من تاريخ الانتهاء قبل الحفظ" if is_ar else "Verify expiry date before saving",
                    value=parsed_default
                )
                qty = st.number_input(
                    "الكمية (كجم)" if is_ar else "Quantity (kg)",
                    min_value=0.05, max_value=20.0, value=0.50, step=0.05
                )
                if st.form_submit_button("💾 حفظ في المؤن" if is_ar else "💾 Save to pantry"):
                    st.session_state.pantry.append({
                        "name": verified_name,
                        "ar": verified_name,
                        "emoji": "📦",
                        "qty": qty,
                        "expiry": verified_expiry,
                        "freshness": 90,
                        "price_per_kg": 0
                    })
                    st.success("تم حفظ المنتج وتاريخ الانتهاء في المؤن." if is_ar else "Product and expiry date saved to your pantry.")
                    st.session_state.pop("last_scan_result", None)

        else:
            st.subheader("🥑 نتيجة النضج والنضارة" if is_ar else "🥑 Ripeness & freshness result")

            product_name = result.get("product_name") or ("منتج غير معروف" if is_ar else "Unknown produce")
            ripeness = result.get("ripeness_level", "unknown")
            score = result.get("freshness_score")
            action = result.get("recommended_action", "unknown")
            confidence = result.get("confidence", 0)

            ripeness_ar = {
                "unripe":"غير ناضج","ripe":"ناضج","very_ripe":"ناضج جداً",
                "overripe":"مفرط النضج","spoiled":"يبدو تالفاً","unknown":"غير واضح"
            }
            action_ar = {
                "wait":"انتظر قبل الاستخدام","use_now":"استخدمه الآن",
                "use_soon":"استخدمه قريباً","discard":"لا تعتمد على الصورة وحدها؛ افحصه قبل الاستخدام",
                "unknown":"غير واضح"
            }

            c1, c2, c3 = st.columns(3)
            c1.metric("المنتج" if is_ar else "Product", product_name)
            c2.metric(
                "مستوى النضج" if is_ar else "Ripeness",
                ripeness_ar.get(ripeness, ripeness) if is_ar else ripeness.replace("_"," ").title()
            )
            c3.metric("الثقة" if is_ar else "Confidence", f"{confidence}%")

            if isinstance(score, (int, float)):
                st.write(("نضارة بصرية تقديرية" if is_ar else "Estimated visual freshness") + f": **{score}%**")
                st.progress(max(0, min(100, int(score))) / 100)

            st.info(
                ("التوصية: " + action_ar.get(action, action))
                if is_ar else
                ("Recommendation: " + action.replace("_"," ").title())
            )
            st.caption(result.get("note", ""))
            st.caption(
                "مهم: هذا تقدير بصري للنضج فقط، وليس فحص سلامة غذائية."
                if is_ar else
                "Important: this is a visual ripeness estimate only, not a food-safety assessment."
            )

            suggested_days = {
                "unripe": 7, "ripe": 4, "very_ripe": 2, "overripe": 1, "spoiled": 0, "unknown": 3
            }.get(ripeness, 3)

            with st.form("save_freshness_scan"):
                verified_name = st.text_input(
                    "اسم المنتج" if is_ar else "Product name",
                    value=product_name
                )
                qty = st.number_input(
                    "الكمية (كجم)" if is_ar else "Quantity (kg)",
                    min_value=0.05, max_value=20.0, value=0.50, step=0.05
                )
                expected_use_by = st.date_input(
                    "تاريخ مقترح للاستخدام" if is_ar else "Suggested use-by date",
                    value=date.today() + timedelta(days=suggested_days)
                )
                if st.form_submit_button("💾 حفظ في المؤن" if is_ar else "💾 Save to pantry"):
                    st.session_state.pantry.append({
                        "name": verified_name,
                        "ar": verified_name,
                        "emoji": "🥬",
                        "qty": qty,
                        "expiry": expected_use_by,
                        "freshness": int(score) if isinstance(score, (int, float)) else 70,
                        "price_per_kg": 0,
                        "ripeness": ripeness
                    })
                    st.success("تم حفظ المنتج ونتيجة النضج في المؤن." if is_ar else "Produce and ripeness result saved to your pantry.")
                    st.session_state.pop("last_scan_result", None)

elif page_idx==5:
    st.title("🍳 "+tr("recipes"))
    st.caption(tr("recipe_title"))
    pantry_names={i["name"] for i in st.session_state.pantry}
    ranked=[]
    for r in RECIPES:
        matches=[i for i in st.session_state.pantry if i["name"] in r["uses"]]
        if matches:
            priority=min((i["expiry"]-date.today()).days for i in matches)
            ranked.append((priority,r,matches))
    if not ranked:
        st.info("Add matching ingredients to your pantry to get suggestions." if st.session_state.lang=="en" else "أضف مكونات إلى المؤن للحصول على اقتراحات.")
    for n,(priority,r,matches) in enumerate(sorted(ranked,key=lambda x:x[0])):
        st.markdown(f"<div class='mooan-card'><div style='font-size:38px'>{r['emoji']}</div><b>{r[st.session_state.lang]}</b><br>⏱ {r['time']} min · 🔥 {r['kcal']} {tr('calories')}<br><small>{'Priority: uses food expiring soon' if st.session_state.lang=='en' else 'أولوية: تستخدم طعاماً قريب الانتهاء'}</small></div>",unsafe_allow_html=True)
        if st.button("🍽️ "+tr("make"),key=f"recipe{n}"):
            # For MVP, the recipe consumes the tracked matching items.
            names={m["name"] for m in matches}
            for idx in reversed(range(len(st.session_state.pantry))):
                if st.session_state.pantry[idx]["name"] in names:
                    use_item(idx)
            st.rerun()

elif page_idx==6:
    st.title("🌱 "+tr("rewards"))
    st.markdown(f"<div class='mooan-soft'><h2>{st.session_state.points} 🌱</h2><p>{tr('reward_title')}</p></div>",unsafe_allow_html=True)
    rewards=[("BHD 1 Marketplace voucher",100),("Free delivery voucher",180),("1 month Premium AI",300)]
    for i,(name,cost) in enumerate(rewards):
        c1,c2=st.columns([4,1]); c1.write(f"**{name}** · {cost} points")
        if c2.button(tr("redeem"),key=f"reward{i}"):
            if st.session_state.points>=cost:
                st.session_state.points-=cost; st.success(tr("reward_ok")); st.rerun()
            else: st.warning(tr("need_points"))

else:
    st.title("👤 "+tr("profile"))
    st.subheader(st.session_state.user["name"])
    st.caption(st.session_state.user["email"])
    st.write(tr("profile_sub"))
    a,b,c=st.columns(3)
    a.metric(tr("points"),st.session_state.points)
    b.metric(tr("saved_food"),f"{st.session_state.food_used_kg:.2f} kg")
    c.metric(tr("save_rate"),f"{saved_rate():.1f}%")
    st.divider()
    st.write("**MOOAN methodology / منهجية مؤن**")
    st.caption(("The MVP counts tracked food as 'used before expiry' only after the user confirms use. Expired/unused food is recorded separately. Loyalty points reward confirmed use, with a higher multiplier for food close to expiry."
                if st.session_state.lang=="en" else
                "تسجل النسخة التجريبية الطعام ضمن «استخدم قبل انتهاء الصلاحية» فقط بعد تأكيد المستخدم. ويسجل الطعام المنتهي أو غير المستخدم بشكل منفصل. وتُمنح نقاط الولاء عند تأكيد الاستخدام مع نقاط إضافية للطعام الأقرب للانتهاء."))

st.divider()
st.caption("MOOAN © 2026 · Bahrain 🇧🇭 · MVP demo")
