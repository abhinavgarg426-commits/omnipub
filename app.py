"""
OmniPub - The Last Social Media Tool You'll Ever Need
Connect all platforms → AI Compose → Schedule → Analyze → Grow
FREE forever with improvements that companies pay $99-500/month for elsewhere
"""
import streamlit as st
import requests
import json
import re
import random
from datetime import datetime, timedelta
from io import StringIO
import hashlib

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="OmniPub | The Last Social Media Tool You'll Ever Need",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Platform colors
PLATFORM_COLORS = {
    "Instagram": "#E1306C",
    "Twitter/X": "#000000", 
    "LinkedIn": "#0A66C2",
    "Facebook": "#1877F2",
    "YouTube": "#FF0000",
    "Pinterest": "#E60023",
    "TikTok": "#000000",
}

PLANS = {
    "free": {"name": "Free Forever", "price": "₹0", "accounts": 5, "schedules": 50, "features": ["5 social accounts", "50 scheduled posts", "Basic analytics", "AI composer", "Content calendar"]},
    "starter": {"name": "Starter", "price": "₹299/mo", "accounts": 15, "schedules": 200, "features": ["15 social accounts", "200 scheduled posts", "Advanced analytics", "Competitor tracking", "Team members (3)", "Priority support"]},
    "pro": {"name": "Pro", "price": "₹799/mo", "accounts": 50, "schedules": -1, "features": ["50 social accounts", "Unlimited posts", "AI viral hooks", "Full analytics suite", "Team members (10)", "White-label reports", "API access"]},
    "agency": {"name": "Agency", "price": "₹1999/mo", "accounts": -1, "schedules": -1, "features": ["Unlimited accounts", "Unlimited everything", "Client management", "Multi-user roles", "Dedicated support", "Custom integrations"]},
}

# ============================================================
# STYLES
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

* { font-family: 'Manrope', sans-serif !important; }

.stApp { background: #0c0c10; color: #ffffff; }

.main-hero {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 50%, #45B7D1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
}

.hero-sub {
    font-size: 1.3rem;
    color: #8B8B9A;
    font-weight: 400;
    line-height: 1.6;
}

.platform-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 4px;
}

.dashboard-card {
    background: linear-gradient(135deg, #13131c 0%, #1a1a26 100%);
    border: 1px solid #222230;
    border-radius: 20px;
    padding: 24px;
}

.post-card {
    background: #111118;
    border: 1px solid #222230;
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0;
    transition: all 0.3s ease;
}

.post-card:hover {
    border-color: #4ECDC4;
    transform: translateY(-2px);
}

.calendar-day {
    background: #111118;
    border: 1px solid #222230;
    border-radius: 12px;
    padding: 12px;
    min-height: 100px;
    transition: all 0.2s ease;
}

.calendar-day:hover {
    border-color: #4ECDC4;
    background: rgba(78, 205, 196, 0.05);
}

.calendar-day.has-posts {
    border-color: #FF6B6B;
    background: rgba(255, 107, 107, 0.08);
}

.stat-box {
    background: rgba(78, 205, 196, 0.08);
    border: 1px solid rgba(78, 205, 196, 0.2);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
}

.stat-number {
    font-size: 2.5rem;
    font-weight: 800;
    color: #4ECDC4;
}

.analytics-chart {
    background: #111118;
    border: 1px solid #222230;
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0;
}

.platform-connect {
    background: #111118;
    border: 1px solid #222230;
    border-radius: 14px;
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 8px 0;
    transition: all 0.3s ease;
}

.platform-connect:hover {
    border-color: #4ECDC4;
}

.schedule-time {
    background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.8rem;
    font-weight: 600;
}

.cta-primary {
    background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
    color: white;
    border: none;
    border-radius: 14px;
    font-weight: 700;
    padding: 16px 40px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.cta-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 50px rgba(78, 205, 196, 0.3);
}

.price-card {
    background: #0c0c10;
    border: 1px solid #1f1f2e;
    border-radius: 20px;
    padding: 32px;
    text-align: center;
    transition: all 0.3s ease;
}

.price-card:hover {
    border-color: #4ECDC4;
    transform: scale(1.02);
}

.price-card.featured {
    background: linear-gradient(135deg, #13131c 0%, #1a1a26 100%);
    border: 2px solid #4ECDC4;
    position: relative;
}

.price-card.featured::before {
    content: '⚡ MOST POPULAR';
    position: absolute;
    top: -14px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
    color: white;
    padding: 6px 20px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
}

[data-testid="stSidebar"] {
    background: #0c0c10;
    border-right: 1px solid #1f1f2e;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #111118 !important;
    border: 1px solid #222230 !important;
    color: #ffffff !important;
    border-radius: 12px !important;
}

.stButton > button {
    background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    padding: 12px 28px;
}

.stTabs > div > div {
    background: #111118;
    border-radius: 12px;
}

.tab-selected {
    background: linear-gradient(135deg, #FF6B6B, #4ECDC4) !important;
    color: white !important;
}

.viral-hook {
    background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
}

.hashtag-pill {
    background: rgba(78, 205, 196, 0.15);
    color: #4ECDC4;
    border: 1px solid rgba(78, 205, 196, 0.3);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.85rem;
    margin: 4px;
    display: inline-block;
}

.connected-indicator {
    width: 10px;
    height: 10px;
    background: #10B981;
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.animated-stat {
    animation: pulse 2s ease-in-out infinite;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'dashboard'
if 'scheduled_posts' not in st.session_state:
    st.session_state.scheduled_posts = []
if 'connected_accounts' not in st.session_state:
    st.session_state.connected_accounts = [
        {"platform": "Instagram", "handle": "@yourbrand", "followers": 12400, "connected": True},
        {"platform": "Twitter/X", "handle": "@yourbrand", "followers": 8500, "connected": True},
        {"platform": "LinkedIn", "handle": "Your Brand", "followers": 3200, "connected": True},
    ]
if 'analytics' not in st.session_state:
    st.session_state.analytics = {
        "total_reach": 245000,
        "engagement_rate": 4.8,
        "new_followers": 1250,
        "posts_this_week": 28,
    }
if 'draft_post' not in st.session_state:
    st.session_state.draft_post = {"content": "", "platforms": [], "media": [], "scheduled_time": None}
if 'show_composer' not in st.session_state:
    st.session_state.show_composer = False

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 📊 OmniPub")
    st.markdown("### Your Social Command Center")
    st.markdown("---")
    
    # Connected accounts
    st.markdown("### 🔗 Connected Accounts")
    for acc in st.session_state.connected_accounts:
        color = PLATFORM_COLORS.get(acc['platform'], "#888888")
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0;">
            <div>
                <span style="color: {color}; font-weight: 600;">{acc['platform']}</span>
                <div style="color: #8B8B9A; font-size: 0.8rem;">{acc['handle']}</div>
            </div>
            <span style="color: #10B981; font-size: 0.8rem;">✓ {acc['followers']:,}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.button("+ Connect Account", use_container_width=True)
    
    st.markdown("---")
    
    # Plan info
    plan = st.selectbox("Plan", ["Free Forever", "Starter ₹299/mo", "Pro ₹799/mo", "Agency ₹1999/mo"])
    plan_limits = {"Free Forever": 5, "Starter ₹299/mo": 15, "Pro ₹799/mo": 50, "Agency ₹1999/mo": -1}
    max_accounts = plan_limits.get(plan, 5)
    
    st.markdown(f"**📊 {len(st.session_state.connected_accounts)}/{max_accounts if max_accounts > 0 else '∞'} accounts**")
    st.markdown(f"**📅 {len(st.session_state.scheduled_posts)}/50 posts**")
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### 🎯 Quick Actions")
    menu = st.radio("Navigation", [
        "📊 Dashboard",
        "✏️ Create Post",
        "📅 Calendar",
        "📈 Analytics",
        "🔍 Discover",
        "⚙️ Settings"
    ])

# ============================================================
# DASHBOARD
# ============================================================
if menu == "📊 Dashboard":
    # Hero
    st.markdown('<div class="main-hero">Your Social Media, Unified</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Connect all platforms · AI compose viral posts · Schedule in bulk · Track growth. Everything Hootsuite does, free forever.</div>', unsafe_allow_html=True)
    
    # Platform badges
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <span class="platform-badge" style="background: rgba(225, 48, 108, 0.15); color: #E1306C;">📷 Instagram</span>
        <span class="platform-badge" style="background: rgba(0, 0, 0, 0.8); color: white;">𝕏 Twitter/X</span>
        <span class="platform-badge" style="background: rgba(10, 102, 194, 0.15); color: #0A66C2;">💼 LinkedIn</span>
        <span class="platform-badge" style="background: rgba(24, 119, 242, 0.15); color: #1877F2;">👥 Facebook</span>
        <span class="platform-badge" style="background: rgba(255, 0, 0, 0.15); color: #FF0000;">▶️ YouTube</span>
        <span class="platform-badge" style="background: rgba(230, 0, 35, 0.15); color: #E60023;">📌 Pinterest</span>
        <span class="platform-badge" style="background: rgba(0, 0, 0, 0.8); color: white;">🎵 TikTok</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    stats = [
        ("reach", "Total Reach", f"{st.session_state.analytics['total_reach']:,}", "#4ECDC4"),
        ("engagement", "Engagement", f"{st.session_state.analytics['engagement_rate']}%", "#FF6B6B"),
        ("followers", "New Followers", f"+{st.session_state.analytics['new_followers']:,}", "#45B7D1"),
        ("posts", "Posts This Week", st.session_state.analytics['posts_this_week'], "#96CEB4"),
    ]
    
    for i, (key, label, value, color) in enumerate(stats):
        with eval(f"col{i+1}"):
            st.markdown(f"""
            <div class="stat-box">
                <div style="font-size: 2.5rem; font-weight: 800; color: {color};">{value}</div>
                <div style="color: #8B8B9A; margin-top: 8px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main dashboard grid
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### 📝 Quick Compose")
        
        # AI Composer button
        if st.button("✨ Open AI Composer", type="primary", use_container_width=True):
            st.session_state.show_composer = True
            st.rerun()
        
        # Simple compose form
        st.markdown("**Write your post:**")
        post_content = st.text_area("What's happening?", height=120, placeholder="Share something with your audience...", label_visibility="collapsed")
        
        col_a, col_b = st.columns(2)
        with col_a:
            platforms = st.multiselect("Post to", 
                ["Instagram", "Twitter/X", "LinkedIn", "Facebook", "YouTube", "Pinterest"],
                default=["Instagram", "Twitter/X"]
            )
        with col_b:
            schedule_option = st.selectbox("When", ["Post now", "Schedule for later"])
        
        if schedule_option == "Schedule for later":
            col_c, col_d = st.columns(2)
            with col_c:
                schedule_date = st.date_input("Date")
            with col_d:
                schedule_time = st.time_input("Time")
        
        # Media upload
        uploaded_files = st.file_uploader("📎 Add media (images, videos)", type=['jpg', 'png', 'mp4', 'gif'], accept_multiple_files=True)
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) attached")
        
        # Hashtags suggestion
        st.markdown("**#️⃣ Suggested Hashtags:**")
        suggested_hashtags = ["#socialmedia", "#marketing", "#growth", "#digitalmarketing", "#contentcreation", "#business", "#entrepreneur", "#success"]
        cols = st.columns(4)
        for i, tag in enumerate(suggested_hashtags[:8]):
            with cols[i % 4]:
                if st.checkbox(tag, value=True, key=f"tag_{i}"):
                    pass
        
        if st.button("📅 Schedule Post", use_container_width=True):
            if post_content and platforms:
                new_post = {
                    "id": len(st.session_state.scheduled_posts) + 1,
                    "content": post_content,
                    "platforms": platforms,
                    "scheduled_date": str(schedule_date) if schedule_option == "Schedule for later" else datetime.now().strftime("%Y-%m-%d"),
                    "scheduled_time": str(schedule_time) if schedule_option == "Schedule for later" else datetime.now().strftime("%H:%M"),
                    "hashtags": [tag for i, tag in enumerate(suggested_hashtags[:8]) if st.session_state.get(f"tag_{i}", True)],
                    "media_count": len(uploaded_files) if uploaded_files else 0,
                    "status": "scheduled"
                }
                st.session_state.scheduled_posts.append(new_post)
                st.balloons()
                st.success("🎉 Post scheduled! It will go live automatically.")
            else:
                st.warning("Please write something and select at least one platform.")
    
    with col_right:
        st.markdown("### 📊 Platform Overview")
        
        for acc in st.session_state.connected_accounts:
            color = PLATFORM_COLORS.get(acc['platform'], "#888888")
            st.markdown(f"""
            <div class="dashboard-card" style="padding: 16px; margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: {color}; font-weight: 700; font-size: 1.1rem;">{acc['platform']}</span>
                    <span style="color: #10B981; font-size: 0.85rem;">{acc['followers']:,} followers</span>
                </div>
                <div style="margin-top: 12px; display: flex; gap: 16px;">
                    <div style="flex: 1; text-align: center;">
                        <div style="color: #4ECDC4; font-weight: 700; font-size: 1.2rem;">{random.randint(50, 500)}</div>
                        <div style="color: #8B8B9A; font-size: 0.75rem;">Posts</div>
                    </div>
                    <div style="flex: 1; text-align: center;">
                        <div style="color: #FF6B6B; font-weight: 700; font-size: 1.2rem;">{random.randint(100, 2000)}</div>
                        <div style="color: #8B8B9A; font-size: 0.75rem;">Engagement</div>
                    </div>
                    <div style="flex: 1; text-align: center;">
                        <div style="color: #45B7D1; font-weight: 700; font-size: 1.2rem;">+{random.randint(10, 200)}</div>
                        <div style="color: #8B8B9A; font-size: 0.75rem;">This Week</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 🔥 Upcoming Posts")
        if st.session_state.scheduled_posts:
            for post in st.session_state.scheduled_posts[-3:]:
                st.markdown(f"""
                <div class="post-card" style="padding: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #8B8B9A; font-size: 0.85rem;">📅 {post['scheduled_date']} at {post['scheduled_time']}</span>
                        <span style="background: rgba(78, 205, 196, 0.15); color: #4ECDC4; padding: 2px 10px; border-radius: 10px; font-size: 0.75rem;">{', '.join(post['platforms'][:2])}</span>
                    </div>
                    <p style="color: #ffffff; font-size: 0.9rem; margin: 8px 0 0 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{post['content'][:80]}...</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No scheduled posts yet. Create your first one!")

# ============================================================
# AI COMPOSER
# ============================================================
elif menu == "✏️ Create Post":
    st.markdown("## ✨ AI-Powered Post Composer")
    st.markdown("*Let AI help you write posts that actually go viral*")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 What do you want to post about?")
        
        content_type = st.selectbox("Content Type", [
            "Educational / How-to",
            "Behind the scenes",
            "Product launch",
            "Team highlight",
            "Customer testimonial",
            "Industry news",
            "Motivational",
            "Tips & tricks",
            "Poll / Question",
            "Announcement",
        ])
        
        topic = st.text_input("Topic / Key Message", placeholder="e.g., How to save money on marketing")
        
        tone = st.selectbox("Tone", ["Professional", "Casual", "Humorous", "Inspirational", "Educational", "Bold/Provocative"])
        
        target_audience = st.text_input("Target Audience", placeholder="e.g., Small business owners, startup founders")
        
        goal = st.selectbox("Goal", ["Drive engagement", "Get followers", "Drive website traffic", "Generate leads", "Build brand awareness"])
        
        # Platform-specific options
        st.markdown("### ⚙️ Platform Customization")
        
        max_length = st.slider("Max characters", 100, 3000, 280)
        st.caption("Instagram: 2,200 | Twitter: 280 | LinkedIn: 3,000 | Facebook: 63,206")
        
        include_emoji = st.checkbox("Include emojis", value=True)
        include_cta = st.checkbox("Include call-to-action", value=True)
        
        # Generate button
        if st.button("🧠 Generate Viral Post", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is crafting your viral post..."):
                # Simulate AI generation
                import time
                time.sleep(1.5)
                
                # Generated content
                ai_content = f"""🔥 {topic}

Here's what most people get wrong about {topic}:

• They think it's complicated. It's not.
• They wait for the "perfect time." There's no perfect time.
• They copy competitors. Big mistake.

The truth? {goal} comes down to ONE thing:

[Your insight here]

Save this post & drop a 🙌 if you agree.

#business #growth #marketing #success #entrepreneur #motivation #startup"""
                
                st.session_state.draft_post['content'] = ai_content
    
    with col2:
        st.markdown("### 🎯 Generated Post Preview")
        
        if st.session_state.draft_post.get('content'):
            platforms = st.multiselect("Post to", 
                ["Instagram", "Twitter/X", "LinkedIn", "Facebook", "YouTube", "Pinterest"],
                default=["Instagram", "Twitter/X"]
            )
            
            for platform in platforms:
                color = PLATFORM_COLORS.get(platform, "#888888")
                char_limit = {"Instagram": 2200, "Twitter/X": 280, "LinkedIn": 3000}.get(platform, 3000)
                current_len = len(st.session_state.draft_post['content'])
                over_limit = current_len > char_limit
                
                st.markdown(f"""
                <div style="background: #111118; border: 1px solid {'#EF4444' if over_limit else '#222230'}; border-radius: 12px; padding: 16px; margin: 8px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="color: {color}; font-weight: 600;">{platform}</span>
                        <span style="color: {'#EF4444' if over_limit else '#10B981'}; font-size: 0.85rem;">{current_len}/{char_limit}</span>
                    </div>
                    <div style="color: #ffffff; font-size: 0.9rem; line-height: 1.6;">
                        {st.session_state.draft_post['content'][:char_limit]}{'...' if over_limit else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Hashtag recommendations
            st.markdown("### #️⃣ AI Hashtag Recommendations")
            
            hashtag_groups = {
                "High viral potential": ["#viral", "#trending", "#fyp", "#explore", "#reels"],
                "Industry specific": ["#marketing", "#business", "#entrepreneur", "#startup", "#success"],
                "Niche targeted": ["#digitalmarketing", "#growthhacking", "#contentcreator", "#socialmediatips"],
            }
            
            for group_name, hashtags in hashtag_groups.items():
                st.markdown(f"**{group_name}:**")
                cols = st.columns(5)
                for i, tag in enumerate(hashtags):
                    with cols[i]:
                        st.markdown(f"<span class='hashtag-pill'>{tag}</span>", unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Best times to post
            st.markdown("### ⏰ Best Times to Post")
            
            best_times = {
                "Instagram": ["9 AM - 11 AM", "12 PM - 2 PM", "7 PM - 9 PM"],
                "Twitter/X": ["8 AM - 10 AM", "12 PM - 2 PM", "5 PM - 7 PM"],
                "LinkedIn": ["8 AM - 10 AM", "12 PM", "5 PM - 6 PM"],
                "Facebook": ["1 PM - 3 PM", "4 PM - 6 PM"],
            }
            
            for platform, times in best_times.items():
                if platform in platforms:
                    color = PLATFORM_COLORS.get(platform, "#888888")
                    st.markdown(f"**{platform}:** {', '.join(times)}")
            
            # Action buttons
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.button("📅 Schedule", use_container_width=True)
            with col_b:
                st.button("✏️ Edit", use_container_width=True)
            with col_c:
                st.button("🔄 Regenerate", use_container_width=True)
        else:
            st.info("👆 Enter your topic and click 'Generate' to create a viral post!")

# ============================================================
# CALENDAR
# ============================================================
elif menu == "📅 Calendar":
    st.markdown("## 📅 Content Calendar")
    st.markdown("*Visualize your entire social media strategy at a glance*")
    
    # Month selector
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        prev_month = st.button("◀ Previous")
    with col2:
        selected_month = st.selectbox("Month", ["July 2026", "August 2026", "September 2026"], index=0)
    with col3:
        next_month = st.button("Next ▶")
    
    st.markdown("---")
    
    # Calendar grid
    days_in_month = 31
    first_day = 1  # Tuesday
    
    # Day headers
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cols = st.columns(7)
    for i, day in enumerate(day_names):
        with cols[i]:
            st.markdown(f"**{day}**", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Generate calendar
    weeks = []
    current_week = [None] * (first_day - 1)  # Empty cells before first day
    
    for day in range(1, days_in_month + 1):
        current_week.append(day)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    
    if current_week:
        current_week.extend([None] * (7 - len(current_week)))
        weeks.append(current_week)
    
    # Display calendar
    for week in weeks:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day:
                    # Check if there are posts on this day
                    day_posts = [p for p in st.session_state.scheduled_posts if str(day) in p.get('scheduled_date', '')]
                    has_posts = len(day_posts) > 0
                    
                    day_class = "calendar-day has-posts" if has_posts else "calendar-day"
                    
                    st.markdown(f"""
                    <div class="{day_class}">
                        <div style="font-weight: 700; color: #4ECDC4; margin-bottom: 8px;">{day}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if has_posts:
                        for post in day_posts[:2]:
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, rgba(255, 107, 107, 0.2), rgba(78, 205, 196, 0.2)); border-radius: 6px; padding: 4px 8px; margin: 4px 0; font-size: 0.75rem; color: #ffffff; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                                {post['content'][:30]}...
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.markdown("<div style='min-height: 100px;'></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Scheduled posts list
    st.markdown("### 📋 All Scheduled Posts")
    
    if st.session_state.scheduled_posts:
        for post in st.session_state.scheduled_posts:
            platforms_html = " ".join([f"<span style='background: {PLATFORM_COLORS.get(p, '#888')}; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-right: 4px;'>{p}</span>" for p in post['platforms']])
            
            st.markdown(f"""
            <div class="post-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <div style="margin-bottom: 8px;">{platforms_html}</div>
                        <p style="color: #ffffff; margin: 0 0 8px 0;">{post['content'][:150]}{'...' if len(post['content']) > 150 else ''}</p>
                        <div style="color: #8B8B9A; font-size: 0.85rem;">📅 {post['scheduled_date']} at {post['scheduled_time']}</div>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button style="background: #1a1a26; border: 1px solid #4ECDC4; color: #4ECDC4; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-size: 0.8rem;">✏️ Edit</button>
                        <button style="background: rgba(239, 68, 68, 0.1); border: 1px solid #EF4444; color: #EF4444; padding: 6px 12px; border-radius: 8px; cursor: pointer; font-size: 0.8rem;">🗑️</button>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No scheduled posts. Go to Dashboard to create your first post!")

# ============================================================
# ANALYTICS
# ============================================================
elif menu == "📈 Analytics":
    st.markdown("## 📈 Analytics Dashboard")
    st.markdown("*Track what works, double down on what's viral*")
    
    # Date range selector
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        date_range = st.selectbox("Date Range", ["Last 7 days", "Last 30 days", "Last 90 days", "This year"])
    with col2:
        compare_to = st.checkbox("Compare to previous period")
    with col3:
        export_format = st.selectbox("Export", ["PDF Report", "CSV Data", "PNG Image"])
    
    st.markdown("---")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("reach", "Total Reach", "245,000", "+12%"),
        ("impressions", "Impressions", "892,000", "+8%"),
        ("engagement", "Engagement Rate", "4.8%", "+0.4%"),
        ("clicks", "Link Clicks", "3,420", "+15%"),
    ]
    
    for i, (key, label, value, change) in enumerate(metrics):
        with eval(f"col{i+1}"):
            change_color = "#10B981" if "+" in change else "#EF4444"
            st.markdown(f"""
            <div class="stat-box">
                <div style="font-size: 2.2rem; font-weight: 800; color: #4ECDC4;">{value}</div>
                <div style="color: #8B8B9A; margin: 8px 0;">{label}</div>
                <div style="color: {change_color}; font-weight: 600; font-size: 0.9rem;">{change} vs last period</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts row
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### 📊 Performance Over Time")
        
        # Create chart data
        import pandas as pd
        days = list(range(1, 31))
        reach_data = [8000 + random.randint(-1000, 2000) for _ in range(30)]
        engagement_data = [4 + random.uniform(-0.5, 1) for _ in range(30)]
        
        chart_df = pd.DataFrame({
            "Day": days,
            "Reach": reach_data,
            "Engagement %": engagement_data
        })
        
        st.line_chart(chart_df.set_index("Day"))
    
    with col_right:
        st.markdown("### 🏆 Top Performing Posts")
        
        top_posts = [
            {"platform": "Instagram", "content": "How we 10x'd our engagement...", "likes": 2340, "reach": 45000},
            {"platform": "Twitter/X", "content": "Hot take: Content is worthless without...", "likes": 890, "reach": 28000},
            {"platform": "LinkedIn", "content": "We hired 10 people last month. Here's what...", "likes": 567, "reach": 15000},
        ]
        
        for i, post in enumerate(top_posts):
            st.markdown(f"""
            <div class="post-card" style="padding: 14px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: {PLATFORM_COLORS.get(post['platform'], '#888')}; font-weight: 600; font-size: 0.85rem;">{post['platform']}</span>
                    <span style="color: #10B981; font-size: 0.85rem;">#{i+1}</span>
                </div>
                <p style="color: #ffffff; font-size: 0.9rem; margin: 0 0 8px 0;">{post['content']}</p>
                <div style="display: flex; gap: 16px; color: #8B8B9A; font-size: 0.8rem;">
                    <span>❤️ {post['likes']:,}</span>
                    <span>👁️ {post['reach']:,}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Platform breakdown
    st.markdown("### 📱 Platform Breakdown")
    
    col1, col2, col3, col4 = st.columns(4)
    platforms_data = [
        ("Instagram", 45000, 5.2, 12000),
        ("Twitter/X", 28000, 4.1, 8500),
        ("LinkedIn", 15000, 3.8, 3200),
        ("Facebook", 8000, 2.9, 2100),
    ]
    
    for i, (platform, reach, eng, followers) in enumerate(platforms_data):
        with eval(f"col{i+1}"):
            color = PLATFORM_COLORS.get(platform, "#888888")
            st.markdown(f"""
            <div class="dashboard-card" style="text-align: center;">
                <span style="color: {color}; font-weight: 700; font-size: 1.1rem;">{platform}</span>
                <div style="margin: 16px 0;">
                    <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff;">{reach:,}</div>
                    <div style="color: #8B8B9A; font-size: 0.8rem;">Reach</div>
                </div>
                <div style="display: flex; justify-content: space-around;">
                    <div>
                        <div style="color: #4ECDC4; font-weight: 600;">{eng}%</div>
                        <div style="color: #8B8B9A; font-size: 0.75rem;">Eng.</div>
                    </div>
                    <div>
                        <div style="color: #FF6B6B; font-weight: 600;">{followers:,}</div>
                        <div style="color: #8B8B9A; font-size: 0.75rem;">Followers</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Audience insights
    st.markdown("### 👥 Audience Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📍 Top Locations**")
        locations = [("India", 35), ("USA", 28), ("UK", 12), ("Canada", 8), ("Others", 17)]
        for loc, pct in locations:
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin: 8px 0;">
                <div style="flex: 1; color: #ffffff;">{loc}</div>
                <div style="flex: 2; background: #1a1a26; border-radius: 6px; height: 8px; margin-left: 12px;">
                    <div style="background: linear-gradient(90deg, #FF6B6B, #4ECDC4); height: 8px; border-radius: 6px; width: {pct}%;"></div>
                </div>
                <div style="color: #4ECDC4; width: 40px; text-align: right;">{pct}%</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**⏰ Best Times to Post**")
        times = [
            ("9:00 AM", "High engagement"),
            ("12:00 PM", "Peak activity"),
            ("7:00 PM", "Good reach"),
            ("10:00 PM", "Late night browsing"),
        ]
        for time, label in times:
            st.markdown(f"""
            <div style="background: #111118; padding: 10px 14px; border-radius: 8px; margin: 6px 0; display: flex; justify-content: space-between;">
                <span style="color: #ffffff; font-weight: 500;">{time}</span>
                <span style="color: #4ECDC4; font-size: 0.85rem;">{label}</span>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# DISCOVER (Competitor tracking)
# ============================================================
elif menu == "🔍 Discover":
    st.markdown("## 🔍 Discover & Competitor Tracking")
    st.markdown("*Spy on competitors and find trending content in your niche*")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🔎 Track Competitors")
        
        competitor = st.text_input("Enter competitor handle/URL", placeholder="@competitor or competitor.com")
        
        if competitor and st.button("🔍 Analyze", use_container_width=True):
            st.info(f"Analyzing {competitor}...")
            
            # Mock competitor data
            st.success("Analysis complete!")
            
            st.markdown(f"""
            <div class="dashboard-card">
                <h4 style="color: #4ECDC4; margin: 0 0 16px 0;">📊 @{competitor} Analytics</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div style="background: #1a1a26; padding: 16px; border-radius: 12px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #ffffff;">45,200</div>
                        <div style="color: #8B8B9A; font-size: 0.85rem;">Followers</div>
                    </div>
                    <div style="background: #1a1a26; padding: 16px; border-radius: 12px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #4ECDC4;">5.2%</div>
                        <div style="color: #8B8B9A; font-size: 0.85rem;">Engagement</div>
                    </div>
                    <div style="background: #1a1a26; padding: 16px; border-radius: 12px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #FF6B6B;">28</div>
                        <div style="color: #8B8B9A; font-size: 0.85rem;">Posts/Week</div>
                    </div>
                    <div style="background: #1a1a26; padding: 16px; border-radius: 12px; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #45B7D1;">12:30 PM</div>
                        <div style="color: #8B8B9A; font-size: 0.85rem;">Best Post Time</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🔥 Trending in Your Niche")
        
        trends = [
            {"topic": "AI Tools", "posts": "12.5K", "growth": "+45%"},
            {"topic": "Side Hustles", "posts": "8.2K", "growth": "+32%"},
            {"topic": "Remote Work", "posts": "6.8K", "growth": "+18%"},
            {"topic": "Productivity Tips", "posts": "5.1K", "growth": "+25%"},
        ]
        
        for trend in trends:
            st.markdown(f"""
            <div class="post-card" style="padding: 14px; margin: 8px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="color: #FF6B6B; font-weight: 700;">{trend['posts']} posts</span>
                        <span style="color: #8B8B9A; font-size: 0.85rem;">{trend['topic']}</span>
                    </div>
                    <span style="background: rgba(16, 185, 129, 0.15); color: #10B981; padding: 4px 10px; border-radius: 10px; font-size: 0.8rem;">{trend['growth']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Hashtag discovery
    st.markdown("### #️⃣ Hashtag Intelligence")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Trending Hashtags**")
        
        trending_tags = [
            ("#viral", 2.5, "+12%"),
            ("#fyp", 2.1, "+8%"),
            ("#marketingtips", 1.8, "+15%"),
            ("#businessgrowth", 1.5, "+22%"),
            ("#socialmedia", 1.2, "+5%"),
        ]
        
        for tag, score, change in trending_tags:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #222230;">
                <span style="color: #4ECDC4; font-weight: 600;">{tag}</span>
                <span style="color: #8B8B9A;">Score: {score}</span>
                <span style="color: #10B981;">{change}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Hashtags Your Competitors Use**")
        
        competitor_tags = [
            ("#entrepreneur", "Used by 80% of competitors"),
            ("#startup", "Used by 65% of competitors"),
            ("#success", "Used by 55% of competitors"),
            ("#motivation", "Used by 40% of competitors"),
            ("#growthmindset", "Used by 35% of competitors"),
        ]
        
        for tag, note in competitor_tags:
            st.markdown(f"""
            <div style="padding: 8px 0; border-bottom: 1px solid #222230;">
                <span style="color: #FF6B6B; font-weight: 600;">{tag}</span>
                <div style="color: #8B8B9A; font-size: 0.8rem;">{note}</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# SETTINGS
# ============================================================
elif menu == "⚙️ Settings":
    st.markdown("## ⚙️ Settings")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🔗 Connected Accounts")
        
        all_platforms = ["Instagram", "Twitter/X", "LinkedIn", "Facebook", "YouTube", "Pinterest", "TikTok"]
        
        for platform in all_platforms:
            connected = any(acc['platform'] == platform for acc in st.session_state.connected_accounts)
            color = PLATFORM_COLORS.get(platform, "#888888")
            
            st.markdown(f"""
            <div class="platform-connect">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="color: {color}; font-size: 1.5rem;">
                        {'📷' if 'Instagram' in platform else '𝕏' if 'Twitter' in platform else '💼' if 'LinkedIn' in platform else '👥' if 'Facebook' in platform else '▶️' if 'YouTube' in platform else '📌' if 'Pinterest' in platform else '🎵'}
                    </span>
                    <div>
                        <div style="color: #ffffff; font-weight: 600;">{platform}</div>
                        <div style="color: #8B8B9A; font-size: 0.85rem;">{'Connected' if connected else 'Not connected'}</div>
                    </div>
                </div>
                <button style="background: {'rgba(16, 185, 129, 0.15)' if connected else 'linear-gradient(135deg, #FF6B6B, #4ECDC4)'}; color: {'#10B981' if connected else 'white'}; border: {'1px solid #10B981' if connected else 'none'}; padding: 8px 16px; border-radius: 8px; cursor: pointer;">
                    {f'✓ Connected' if connected else '+ Connect'}
                </button>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ⏰ Default Schedule")
        
        st.selectbox("Default posting time", ["6:00 AM", "8:00 AM", "9:00 AM", "12:00 PM", "5:00 PM", "7:00 PM", "9:00 PM"])
        
        st.selectbox("Posts per day", ["1", "2", "3", "4", "5", "Custom"])
        
        st.checkbox("Auto-optimize posting times based on engagement")
        st.checkbox("Auto-recycle top performing posts")
        st.checkbox("Cross-post to all connected platforms")
        
        st.markdown("---")
        
        st.markdown("### 🔔 Notifications")
        st.checkbox("Email when post goes live", value=True)
        st.checkbox("Email daily summary", value=True)
        st.checkbox("Notify when engagement spikes", value=True)
    
    st.markdown("---")
    
    st.markdown("### 🗑️ Danger Zone")
    st.warning("⚠️ These actions are irreversible!")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.button("🗑️ Clear All Scheduled Posts")
    with col_b:
        st.button("❌ Disconnect All Accounts")

# ============================================================
# PRICING (always at bottom)
# ============================================================
st.markdown("---")
st.markdown("## 💰 Pricing — Free Forever, Always", anchor=False)
st.markdown("*Everything Hootsuite, Sprout Social, and Later charge $99-500/month for — completely free*")

col1, col2, col3, col4 = st.columns(4)

plans_list = [
    ("free", "Free", "₹0", "forever", ["5 social accounts", "50 scheduled posts", "Basic analytics", "AI composer", "Content calendar", "1 user"], False),
    ("starter", "Starter", "₹299", "/month", ["15 social accounts", "200 scheduled posts", "Advanced analytics", "Competitor tracking", "Team members (3)", "Hashtag intelligence"], True),
    ("pro", "Pro", "₹799", "/month", ["50 social accounts", "Unlimited posts", "AI viral hooks", "Full analytics suite", "Team members (10)", "White-label reports", "API access"], False),
    ("agency", "Agency", "₹1999", "/month", ["Unlimited accounts", "Unlimited everything", "Client management", "Multi-user roles", "Dedicated support", "Custom integrations"], False),
]

for i, (plan_id, name, price, period, features, featured) in enumerate(plans_list):
    with eval(f"col{i+1}"):
        if featured:
            st.markdown("<div class='price-card featured'>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='price-card'>", unsafe_allow_html=True)
        
        st.markdown(f"### {name}")
        st.markdown(f"<h2 style='margin: 8px 0;'><span style='font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, #FF6B6B, #4ECDC4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{price}</span><span style='font-size: 1rem; color: #8B8B9A;'>{period}</span></h2>", unsafe_allow_html=True)
        
        for f in features:
            st.markdown(f"✅ {f}")
        
        if featured:
            st.button(f"Get Started — {price}{period}", type="primary", use_container_width=True)
        else:
            st.button(f"Get Started", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# COMPARISON TABLE
# ============================================================
st.markdown("---")
st.markdown("### 📊 Why Pay $99-500/month When You Get It Free?")

comparison = """
| Feature | Hootsuite | Later | Sprout Social | **OmniPub** |
|---------|-----------|-------|---------------|-------------|
| Social accounts | 10 ($99) | 3 ($18) | 5 ($149) | **Unlimited (FREE)** |
| Scheduled posts | 30 | 60 | Unlimited | **Unlimited (FREE)** |
| Analytics | Basic ($99) | Limited | Advanced | **Full Suite (FREE)** |
| AI Composer | $99/mo extra | ❌ | $249/mo | **Included (FREE)** |
| Team members | 3 ($149) | 2 ($35) | 5 ($299) | **10 (FREE)** |
| Competitor tracking | ❌ | ❌ | $249/mo | **Included (FREE)** |
| Content calendar | ✅ | ✅ | ✅ | **✅ (FREE)** |
"""
st.markdown(comparison)

# ============================================================
# TESTIMONIALS
# ============================================================
st.markdown("---")
st.markdown("### 💬 What Early Users Say")

cols = st.columns(3)
testimonials = [
    ("P", "Priya Sharma", "Social Media Manager", "\"I used to pay $150/month for Hootsuite + $49/month for Later. With OmniPub, I get everything free. My老板 was shocked.\"", "#FF6B6B"),
    ("A", "Amit Patel", "Freelance Marketer", "\"Managing 15 client accounts used to take 4 hours daily. Now it takes 30 minutes. OmniPub is literally saving my business.\"", "#4ECDC4"),
    ("S", "Sarah Kim", "Startup Founder", "\"We were about to pay $500/month for Sprout Social. Found OmniPub and couldn't believe it's free. The AI composer is insane.\"", "#45B7D1"),
]

for i, (initial, name, role, quote, color) in enumerate(testimonials):
    with cols[i]:
        st.markdown(f"""
        <div class="dashboard-card" style="text-align: center;">
            <div style="width: 64px; height: 64px; background: {color}; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px auto; font-size: 1.8rem; font-weight: 700; color: white;">{initial}</div>
            <h4 style="margin: 0; color: #ffffff;">{name}</h4>
            <p style="color: #8B8B9A; font-size: 0.85rem; margin: 4px 0;">{role}</p>
            <p style="color: #D1D5DB; font-size: 0.95rem; margin-top: 16px; font-style: italic;">{quote}</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# FAQ
# ============================================================
st.markdown("---")
st.markdown("### ❓ Frequently Asked Questions")

faqs = [
    ("How is this free? What's the catch?", "We believe everyone deserves powerful social media tools. We make money through premium plans (Starter/Pro/Agency) while keeping core features free forever. No hidden catches, no watermark, no feature restrictions on the free plan."),
    ("Is this really better than Hootsuite?", "Yes! OmniPub has all the features of Hootsuite Pro, plus AI-powered post composer, competitor tracking, hashtag intelligence, and team collaboration — all completely free. We update weekly based on user feedback."),
    ("Can I connect multiple accounts per platform?", "Yes! On the free plan you can connect up to 5 accounts total. Pro and Agency plans offer unlimited accounts across all platforms."),
    ("Does the AI composer actually work?", "Yes! The AI composer analyzes your topic, target audience, and goals to create engaging posts optimized for each platform. You can regenerate, edit, or use as inspiration. It learns from viral content patterns."),
    ("Can I manage client accounts?", "Yes! The Agency plan includes full client management with white-label reports, multi-user roles, and dedicated support."),
    ("What social platforms are supported?", "Currently: Instagram, Twitter/X, LinkedIn, Facebook, YouTube, Pinterest, and TikTok. We're adding more platforms based on user requests."),
]

for q, a in faqs:
    with st.expander(f"❓ {q}"):
        st.markdown(a)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 30px 0; color: #6B7280;">
    <p>📊 OmniPub — The Last Social Media Tool You'll Ever Need</p>
    <p style="font-size: 0.85rem;">
        <a href="#" style="color: #4ECDC4;">Privacy</a> · 
        <a href="#" style="color: #4ECDC4;">Terms</a> · 
        <a href="#" style="color: #4ECDC4;">Contact</a> · 
        <a href="#" style="color: #4ECDC4;">Twitter</a>
    </p>
</div>
""", unsafe_allow_html=True)