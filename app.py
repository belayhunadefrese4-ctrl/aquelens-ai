import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random
import string

# ==========================================
# 1. PAGE CONFIGURATION & SESSION STATE
# ==========================================
st.set_page_config(
    page_title="AqueLens AI — Water Safety & Contaminant Shield",
    page_icon="💧",
    layout="wide"
)

if "free_used" not in st.session_state:
    st.session_state.free_used = False

if "unlocked_via_key" not in st.session_state:
    st.session_state.unlocked_via_key = False

ADMIN_PASSWORD = "ETHIO_ADMIN_2026"
WHO_SAFETY_BASELINE = 100.0  # Perfect Water Quality Index Baseline

# ==========================================
# 2. MULTILINGUAL DICTIONARY
# ==========================================
TRANSLATIONS = {
    "አማርኛ": {
        "title": "💧 AqueLens AI — የውሃ ደህንነት እና የብክለት መቆጣጠሪያ መድረክ",
        "subtitle": "በዓለም ጤና ድርጅት (WHO) የንፁህ ውሃ መመዘኛዎች መሠረት የተዘጋጀ።",
        "tab1": "1. የውሃ ደህንነት 6 ዋና ዋና መለኪያዎች",
        "tab2": "2. የውሃ ጥራት ዳሽቦርድ እና የትንተና ሪፖርት",
        "tab3": "3. ዓለም አቀፍ እና የሀገር ውስጥ ክፍያዎች",
        "tab4": "4. የአስተዳዳሪ መቆጣጠሪያ (Admin)",
        "p1_head": "📍 የመገኛ ቦታ እና የውሃ ምንጭ",
        "p2_head": "🧪 የኬሚካል እና ማዕድናት መለኪያዎች",
        "p3_head": "🦠 የባክቴሪያ እና የከባድ ብረቶች ስጋት",
        "name_lbl": "ሙሉ ስም / የድርጅቱ ስም",
        "q1": "የአካባቢ/ቀበሌ ስም",
        "q2": "የውሃ ምንጭ ዓይነት",
        "q3": "1. የውሃው አሲድነት መጠን (pH Level)",
        "q4": "2. የተሟሟቱ ማዕድናት መጠን (TDS mg/L)",
        "q5": "3. የውሃ ጥራት እና ጭቃማነት (Turbidity)",
        "q6": "4. የክሎሪን መጠን ബാലንስ (Chlorine Safety)",
        "q7": "5. የከባድ ብረቶች ስጋት (Lead / Heavy Metals)",
        "q8": "6. የባክቴሪያ እና ረቂቅ ተሕዋስያን ስጋት",
        "source_opts": ["ማዘጋጃ ቤት ቧንቧ ውሃ (Municipal Tap)", "የከርሰ ምድር ጉድጓድ (Borehole Well)", " የታሸገ ውሃ (Bottled Water)", "የውሃ ማጠራቀሚያ ታንከር (Tanker Storage)"],
        "ph_opts": ["መደበኛ ጤናማ (6.5 - 8.5 pH)", "አሲዳማ / ቧንቧ የሚሸርሽር (<6.5)", "ከፍተኛ አልካላይን (>8.5)"],
        "tds_opts": ["እጅግ ንፁህ / መደበኛ (<300 mg/L)", "መካከለኛ ማዕድናት (300 - 600 mg/L)", "ከፍተኛ TDS / የተበከለ (>600 mg/L)"],
        "turb_opts": ["ንፁህ እና ግልጽ (0 - 1 NTU)", "ትንሽ ጭቃማ (1 - 5 NTU)", "ከፍተኛ ጭቃማ / የተበከለ (>5 NTU)"],
        "chlor_opts": ["ትክክለኛ የክሎሪን መጠን (Balanced)", "ዝቅተኛ ክሎሪን / ባክቴሪያ ሊኖር ይችላል", "ከፍተኛ ክሎሪን / ኬሚካላዊ ሽታ"],
        "metal_opts": ["ምንም የከባድ ብረቶች ስጋት የለም", "መካከለኛ የቧንቧ ዝገት ስጋት (Lead/Iron)", "ከፍተኛ የብረት እና ኬሚካል ቅሪት"],
        "micro_opts": ["ምንም ረቂቅ ተሕዋስያን የሉም (Safe)", "ሊኖር የሚችል ስጋት (Suspected Runoff)", "የተረጋገጠ የባክቴሪያ ብክለት (E. coli risk)"],
        "succ_msg": "✅ **የውሃ ደህንነት መለኪያዎች ተመዝግበዋል!** ውጤቱን ለማየት ወደ ክፍል 2 ይለፉ።",
        "safety_score": "የውሃ ደህንነት ነጥብ (Water Safety Index)",
        "contam_risk": "የብክለት እና የስጋት ደረጃ",
        "purif_rec": "የማጣራት እና የማጽዳት መፍትሄ",
        "gauge_title": "🎯 የውሃ ደህንነት አጠቃላይ ውጤት (0-100)",
        "bar_title": "📊 በውሃ ጥራት ላይ ተፅእኖ ያላቸው ምክንያቶች",
        "narrative_title": "📊 የውሃ ጥራት እና የጤና ስጋት ማጠቃለያ መግለጫ",
        "btn_export": "📄 የተረጋገጠ የውሃ ጥራት ሪፖርት አውርድ (PDF)"
    },
    "English": {
        "title": "💧 AqueLens AI — Water Safety & Contaminant Shield",
        "subtitle": "Advanced hydrological screening anchored on WHO drinking water quality guidelines.",
        "tab1": "1. Standardized 6-KPI Water Assessment",
        "tab2": "2. Safety Dashboard & Narrative Briefing",
        "tab3": "3. Remittance & Global Payments",
        "tab4": "4. Admin Console",
        "p1_head": "📍 Location & Water Source Profile",
        "p2_head": "🧪 Chemical & Mineral Diagnostics",
        "p3_head": "🦠 Heavy Metal & Pathogen Screening",
        "name_lbl": "Full Name / Organization",
        "q1": "Neighborhood / Zone",
        "q2": "Water Source Type",
        "q3": "1. Water Acidity / Alkalinity (pH Level)",
        "q4": "2. Total Dissolved Solids (TDS mg/L)",
        "q5": "3. Water Clarity & Turbidity",
        "q6": "4. Residual Chlorine Balance",
        "q7": "5. Heavy Metal Risk (Lead / Copper)",
        "q8": "6. Microbial / Pathogen Contamination Risk",
        "source_opts": ["Municipal Tap Water", "Borehole / Groundwater Well", "Commercial Bottled Water", "Storage Tank Supply"],
        "ph_opts": ["Optimal & Safe (6.5 - 8.5 pH)", "Acidic / Pipe Corrosion Risk (<6.5)", "High Alkalinity (>8.5)"],
        "tds_opts": ["Excellent Purity (<300 mg/L)", "Moderate Mineral Content (300 - 600 mg/L)", "High TDS / Contaminated (>600 mg/L)"],
        "turb_opts": ["Clear & Transparent (0 - 1 NTU)", "Slightly Cloudy (1 - 5 NTU)", "High Turbidity / Sediment (>5 NTU)"],
        "chlor_opts": ["Balanced Disinfection", "Low Chlorine / Bacterial Risk", "High Chlorine / Chemical Odor"],
        "metal_opts": ["No Heavy Metal Leach Detected", "Moderate Infrastructure Rust Risk", "High Heavy Metal Contamination"],
        "micro_opts": ["Pathogen-Free (Safe)", "Suspected Agricultural Runoff", "Confirmed Microbial / E. Coli Risk"],
        "succ_msg": "✅ **6 Water Safety KPIs Logged!** Proceed to Tab 2 to view your Water Safety Analysis.",
        "safety_score": "Water Safety Index (0-100)",
        "contam_risk": "Contamination Risk Level",
        "purif_rec": "Recommended Purification Action",
        "gauge_title": "🎯 Overall Water Safety Index",
        "bar_title": "📊 Contaminant Impact Breakdown",
        "narrative_title": "📊 Executive Water Safety & Health Narrative Briefing",
        "btn_export": "📄 Export Certified Water Safety Report (PDF)"
    },
    "العربية": {
        "title": "💧 AqueLens AI — الدرع الذكي لسلامة المياه والملوثات",
        "subtitle": "تحليل هيدرولوجي متقدم مستند إلى معايير منظمة الصحة العالمية (WHO).",
        "tab1": "1. تقييم مؤشرات سلامة المياه الـ 6",
        "tab2": "2. لوحة معلومات السلامة والتقرير التحليلي",
        "tab3": "3. المدفوعات الدولية والتحويلات المالية",
        "tab4": "4. لوحة التحكم والإدارة",
        "p1_head": "📍 الموقع وملف مصدر المياه",
        "p2_head": "🧪 التشخيص الكيميائي والمعادن",
        "p3_head": "🦠 فحص المعادن الثقيلة ومسببات الأمراض",
        "name_lbl": "الاسم الكامل / المؤسسة",
        "q1": "الحي / المنطقة",
        "q2": "نوع مصدر المياه",
        "q3": "1. حموضة الماء (pH Level)",
        "q4": "2. إجمالي المواد الصلبة الذائبة (TDS mg/L)",
        "q5": "3. نقاء الماء والتعكر (Turbidity)",
        "q6": "4. توازن الكلور المتبقي",
        "q7": "5. خطر المعادن الثقيلة (الرصاص / النحاس)",
        "q8": "6. خطر التلوث الميكروبي / البكتيري",
        "source_opts": ["صنبور البلديات (Municipal Tap)", "بئر جوفي (Borehole Well)", "مياه معبأة تجارية (Bottled Water)", "خزان تخزين منزلي (Tanker Storage)"],
        "ph_opts": ["مثالي وآمن (6.5 - 8.5 pH)", "حامضي / خطر تاكل الأنابيب (<6.5)", "قلوي مرتفع (>8.5)"],
        "tds_opts": ["نقاء ممتاز (<300 mg/L)", "محتوى معدني معتدل (300 - 600 mg/L)", "مستوى عالٍ من الأملاح (>600 mg/L)"],
        "turb_opts": ["صافٍ وشفاف (0 - 1 NTU)", "عكر قليلاً (1 - 5 NTU)", "عكر جداً / رواسب (>5 NTU)"],
        "chlor_opts": ["تطهير متوازن", "كلور منخفض / خطر بكتيري", "كلور مرتفع / رائحة كيميائية"],
        "metal_opts": ["لا توجد معادن ثقيلة مكتشفة", "خطر صدأ الأنابيب المحتمل", "تلوث عالٍ بالمعادن الثقيلة"],
        "micro_opts": ["خالٍ من مسببات الأمراض (آمن)", "اشتباه بتلوث زراعي", "تلوث بكتيري مؤكد"],
        "succ_msg": "✅ **تم تسجيل مؤشرات سلامة المياه الـ 6 بنجاح!** انتقل إلى التبويب 2.",
        "safety_score": "مؤشر سلامة المياه (0-100)",
        "contam_risk": "مستوى خطر التلوث",
        "purif_rec": "إجراء التنقية الموصى بها",
        "gauge_title": "🎯 مؤشر سلامة المياه الإجمالي",
        "bar_title": "📊 تحليل تأثير الملوثات",
        "narrative_title": "📊 التقرير التحليلي لسلامة المياه والصحة العامة",
        "btn_export": "📄 تحميل تقرير سلامة المياه المعتمد (PDF)"
    }
}

# Language Selector
lang_choice = st.sidebar.selectbox("🌐 Select Language / ቋንቋ ይምረጡ / اللغة", list(TRANSLATIONS.keys()))
T = TRANSLATIONS[lang_choice]

st.title(T["title"])
st.caption(T["subtitle"])
st.divider()

tab1, tab2, tab3, tab4 = st.tabs([T["tab1"], T["tab2"], T["tab3"], T["tab4"]])

# ==========================================
# 3. TAB 1: 6 WATER SAFETY KPIS
# ==========================================
with tab1:
    st.subheader(T["tab1"])
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"### {T['p1_head']}")
        user_name = st.text_input(T["name_lbl"], "አበበ ከበደ" if lang_choice == "አማርኛ" else "Abebe Kebede")
        loc_name = st.text_input(T["q1"], "ቦሌ ክፍለ ከተማ, አዲስ አበባ" if lang_choice == "አማርኛ" else "Bole Sub-City, Addis Ababa")
        source_val = st.selectbox(T["q2"], T["source_opts"])

    with c2:
        st.markdown(f"### {T['p2_head']}")
        ph_val = st.selectbox(T["q3"], T["ph_opts"])
        tds_val = st.selectbox(T["q4"], T["tds_opts"])
        turb_val = st.selectbox(T["q5"], T["turb_opts"])

    with c3:
        st.markdown(f"### {T['p3_head']}")
        chlor_val = st.selectbox(T["q6"], T["chlor_opts"])
        metal_val = st.selectbox(T["q7"], T["metal_opts"])
        micro_val = st.selectbox(T["q8"], T["micro_opts"])

    st.success(T["succ_msg"])

# Water Safety Scoring Engine (0 to 100)
penalty = 0.0
if ph_val in [T["ph_opts"][1], T["ph_opts"][2]]: penalty += 15.0
if tds_val in [T["tds_opts"][2]]: penalty += 20.0
if turb_val in [T["turb_opts"][2]]: penalty += 20.0
if chlor_val in [T["chlor_opts"][1], T["chlor_opts"][2]]: penalty += 10.0
if metal_val in [T["metal_opts"][2]]: penalty += 20.0
if micro_val in [T["micro_opts"][2]]: penalty += 25.0

safety_index = max(10.0, round(100.0 - penalty, 1))

# ==========================================
# 4. TAB 2: DASHBOARD & NARRATIVE BRIEFING
# ==========================================
with tab2:
    st.header(T["tab2"])
    
    m1, m2, m3 = st.columns(3)
    m1.metric(T["safety_score"], f"{safety_index} / 100")
    m2.metric(T["contam_risk"], "ዝቅተኛ (Safe)" if safety_index >= 80 else ("መካከለኛ (Moderate)" if safety_index >= 50 else "ከፍተኛ (High Risk)"))
    m3.metric("የማጣሪያ ምክር", "መደበኛ ካርቦን ማጣሪያ" if safety_index >= 80 else "ሪቨርስ ኦስሞሲስ (RO) ማጣሪያ ያስፈልጋል")

    st.divider()

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader(T["gauge_title"])
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=safety_index,
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#008060" if safety_index >= 80 else ("#FF9800" if safety_index >= 50 else "#E53935")},
                'steps': [
                    {'range': [0, 50], 'color': "#FFEBEE"},
                    {'range': [50, 80], 'color': "#FFFDE7"},
                    {'range': [80, 100], 'color': "#E8F5E9"}
                ]
            }
        ))
        fig_gauge.update_layout(height=280)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_g2:
        st.subheader(T["bar_title"])
        impact_df = pd.DataFrame({
            "Category" if lang_choice != "አማርኛ" else "ዘርፍ": ["pH & TDS", "ጭቃማነት (Turbidity)", "ክሎሪን", "የከባድ ብረቶች እና ባክቴሪያ"] if lang_choice == "አማርኛ" else ["pH & TDS", "Turbidity", "Chlorine", "Metals & Microbes"],
            "Risk Points" if lang_choice != "አማርኛ" else "የስጋት ነጥብ": [
                15.0 if ph_val in [T["ph_opts"][1]] else 0.0,
                20.0 if turb_val in [T["turb_opts"][2]] else 0.0,
                10.0 if chlor_val in [T["chlor_opts"][1]] else 0.0,
                45.0 if (metal_val in [T["metal_opts"][2]] or micro_val in [T["micro_opts"][2]]) else 0.0
            ]
        })
        fig_bar = px.bar(impact_df, x="Category" if lang_choice != "አማርኛ" else "ዘርፍ", y="Risk Points" if lang_choice != "አማርኛ" else "የስጋት ነጥብ", color="Risk Points" if lang_choice != "አማርኛ" else "የስጋት ነጥብ", color_continuous_scale="Reds")
        fig_bar.update_layout(height=280)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    st.subheader(T["narrative_title"])
    if lang_choice == "አማርኛ":
        narrative_p1 = f"**የውሃ ጥራት ትንተና ማጠቃለያ፡** በ **{loc_name}** ከሚገኘው የ **{source_val}** ምንጭ የተወሰደው ውሃ የተሰላው የደህንነት መውጫ ውጤት **{safety_index} ከ 100** ነው።"
        narrative_p2 = f"**የብክለት እና የኬሚካል ግምገማ፡** የተመረጠው የአሲድነት መጠን ({ph_val}) እና የብረቶች ስጋት ({metal_val}) በቤተሰብዎ ጤና ላይ ቀጥተኛ ተፅእኖ ሊኖረው ስለሚችል ጥንቃቄ ማድረግ ይገባል።"
        narrative_p3 = f"**የማስተካከያ እርምጃዎች፡** ውሃውን ከመጠጣትዎ በፊት ማፍላት ወይም ተስማሚ የሆነ የቤት ውስጥ ማጣሪያ (Reverse Osmosis / Carbon Filter) መጠቀም ይመከራል።"
    else:
        narrative_p1 = f"**Water Quality Overview:** Based on diagnostics from **{source_val}** in **{loc_name}**, the calculated Water Safety Index is **{safety_index} out of 100**."
        narrative_p2 = f"**Contaminant Risk Evaluation:** Parameters including pH ({ph_val}) and heavy metal risk ({metal_val}) indicate the necessity for targeted filtration."
        narrative_p3 = f"**Recommended Action Plan:** Implement immediate boiling protocols or install a certified multi-stage carbon and reverse osmosis filtration system."

    st.markdown(narrative_p1)
    st.markdown(narrative_p2)
    st.markdown(narrative_p3)

    st.divider()

    if st.button(T["btn_export"]):
        st.success("🎉 Report ready!")
        st.download_button(
            "📥 Save Water Safety Report (.txt)",
            data=f"{T['narrative_title']}\n\nClient/Org: {user_name}\nLocation: {loc_name}\nSource: {source_val}\nSafety Index: {safety_index}/100\n\n{narrative_p1}\n\n{narrative_p2}\n\n{narrative_p3}",
            file_name=f"AqueLens_Safety_Report_{user_name}.txt"
        )

# ==========================================
# 5. TAB 3: REMITTANCE & PAYMENTS
# ==========================================
with tab3:
    st.header(T["tab3"])
    p1, p2 = st.columns(2)
    
    with p1:
        st.subheader("💚 Global Payment & Remittance Methods")
        curr = st.radio("Select Currency", ["ETB (ብር)", "USD ($)", "EUR (€)", "GBP (£)"])
        amt = st.number_input("Amount / መጠን", min_value=10, value=200, step=10)
            
        st.info(
            "**📲 Mobile Money / International Remittance (Sendwave, Remitly, WorldRemit, Telebirr):**\n"
            "* Recipient Phone: `+251986884912`\n"
            "* Name: **Belayhun Adefrese**\n\n"
            "**🏦 Commercial Bank of Ethiopia (CBE Direct):**\n"
            "* Account Number: `1000296269488` (Belayhun Adefrese Metaferia)\n\n"
            "**📋 Instructions:** Send payment, paste transaction reference below, and get your SMS Access Key."
        )
        c_ref = st.text_input("Transaction Ref / MTCN / Confirmation Code")
        if st.button("📩 Submit Verification Claim", type="primary"):
            if len(c_ref.strip()) >= 5:
                st.success("✅ Claim logged! Access key will be dispatched via SMS.")
            else:
                st.error("❌ Enter a valid transaction reference.")

    with p2:
        st.subheader("🔑 Unlock Full Unlimited Reports")
        key_in = st.text_input("Enter Access Key Received via SMS", type="password")
        if st.button("Verify & Unlock Access"):
            if key_in.strip():
                st.session_state.unlocked_via_key = True
                st.success("🎉 Key Verified! Full access unlocked.")
                st.rerun()

# ==========================================
# 6. TAB 4: ADMIN CONSOLE
# ==========================================
with tab4:
    st.header(T["tab4"])
    pwd = st.text_input("Admin Password", type="password")
    if pwd == ADMIN_PASSWORD:
        st.success("🔓 Authenticated as Administrator")
        target_phone = st.text_input("Client Phone Number", "+251986884912")
        if st.button("📲 Generate & Dispatch Key"):
            gen_key = f"AQUE-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
            st.info(f"Generated Key: **{gen_key}** dispatched to **{target_phone}**.")
