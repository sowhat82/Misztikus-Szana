import streamlit as st
import random
from datetime import datetime
import calendar

# Page configuration
st.set_page_config(
    page_title="Misztikus Szana - Spiritual Advisor",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Auto-scroll to top on stage change
st.markdown("""
<script>
    window.scrollTo(0, 0);
</script>
""", unsafe_allow_html=True)

# Custom CSS for vintage gypsy style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Uncial+Antiqua&display=swap');

    .stApp {
        background: linear-gradient(135deg, #2d1b00 0%, #4a0404 50%, #1a0a00 100%);
        color: #f4e4c1;
    }

    .main-title {
        font-family: 'Uncial Antiqua', cursive;
        text-align: center;
        font-size: 4em;
        color: #ffd700;
        text-shadow: 3px 3px 6px #000, 0 0 20px #ff6600;
        margin-bottom: 10px;
        letter-spacing: 3px;
        white-space: nowrap;
    }

    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5em;
            white-space: normal;
        }
    }

    .subtitle {
        font-family: 'Cinzel', serif;
        text-align: center;
        font-size: 1.5em;
        color: #d4af37;
        font-style: italic;
        margin-bottom: 30px;
    }

    .szana-speech {
        font-family: 'Cinzel', serif;
        background: linear-gradient(135deg, #3d1f00, #5d2f00);
        border: 3px solid #d4af37;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        font-size: 1.2em;
        color: #f4e4c1;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.3);
        line-height: 1.6;
    }

    .reading-box {
        font-family: 'Cinzel', serif;
        background: linear-gradient(135deg, #1a0a00, #2d1b00);
        border: 2px solid #d4af37;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        color: #f4e4c1;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
    }

    .token-display {
        font-family: 'Cinzel', serif;
        background: linear-gradient(135deg, #4a0404, #2d0202);
        border: 2px solid #ffd700;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        font-size: 1.3em;
        color: #ffd700;
        margin: 10px 0;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
    }

    .card-deck {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
        margin: 20px 0;
    }

    .tarot-card {
        width: 100px;
        height: 150px;
        background: linear-gradient(135deg, #2d1b00, #4a2f00);
        border: 2px solid #d4af37;
        border-radius: 5px;
        cursor: pointer;
        transition: transform 0.3s;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2em;
    }

    .fortune-cookie {
        font-family: 'Cinzel', serif;
        background: #f4e4c1;
        color: #2d1b00;
        border: 2px solid #d4af37;
        border-radius: 10px;
        padding: 20px;
        margin: 20px auto;
        max-width: 500px;
        text-align: center;
        font-size: 1.1em;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
    }

    div[data-testid="stButton"] button {
        font-family: 'Cinzel', serif;
        background: linear-gradient(135deg, #d4af37, #ffd700);
        color: #2d1b00;
        border: 2px solid #ffd700;
        border-radius: 10px;
        padding: 10px 25px;
        font-size: 1.1em;
        font-weight: bold;
        transition: all 0.3s;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
    }

    div[data-testid="stButton"] button:hover {
        background: linear-gradient(135deg, #ffd700, #d4af37);
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.6);
        transform: scale(1.05);
    }

    .stTextInput input {
        background-color: #2d1b00;
        color: #f4e4c1;
        border: 2px solid #d4af37;
        border-radius: 5px;
        font-family: 'Cinzel', serif;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tokens' not in st.session_state:
    st.session_state.tokens = 3  # Start with 3 free tokens
if 'session_readings' not in st.session_state:
    st.session_state.session_readings = 0
if 'stage' not in st.session_state:
    st.session_state.stage = 'welcome'
if 'user_name' not in st.session_state:
    st.session_state.user_name = ''
if 'birth_date' not in st.session_state:
    st.session_state.birth_date = None
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = None
if 'tarot_selected' not in st.session_state:
    st.session_state.tarot_selected = False
if 'dice_rolled' not in st.session_state:
    st.session_state.dice_rolled = False
if 'orb_burst' not in st.session_state:
    st.session_state.orb_burst = False
if 'selected_card' not in st.session_state:
    st.session_state.selected_card = None
if 'dice_result' not in st.session_state:
    st.session_state.dice_result = None
if 'orb_result' not in st.session_state:
    st.session_state.orb_result = None

# Tarot card meanings with visual symbols and short labels
TAROT_CARDS = {
    "The Sun": ("☉", "joy and success", "Sun"),
    "The Star": ("★", "hope and renewal", "Star"),
    "The Moon": ("☽", "illusion and intuition", "Moon"),
    "Yin Yang": ("☯", "balance and harmony", "Balance"),
    "The Fire": ("🜂", "passion and transformation", "Fire"),
    "The Eye": ("◉", "insight and awareness", "Eye"),
    "The Cosmos": ("✦", "infinite possibilities", "Cosmos"),
    "The North Star": ("✧", "guidance and direction", "N-Star"),
    "The Planet": ("♃", "cycles and expansion", "Planet"),
    "The Phoenix": ("Ψ", "rebirth and renewal", "Phoenix"),
    "The Teal Sun": ("☼", "vitality and energy", "T-Sun"),
    "The Red Sun": ("⊙", "power and strength", "R-Sun"),
    "The Crystal": ("◆", "clarity and truth", "Crystal"),
    "The Sacred Eye": ("⊕", "divine wisdom", "S-Eye"),
    "The Serpent": ("∿", "transformation and healing", "Serpent"),
    "The Crescent": ("☾", "intuition and mystery", "Crescent"),
    "The Lovers": ("♡", "harmony and choices", "Lovers"),
    "The Hermit": ("✵", "soul searching and introspection", "Hermit"),
    "The Chariot": ("⚡", "willpower and determination", "Chariot"),
    "The Tower": ("△", "sudden change and revelation", "Tower"),
    "The Wheel": ("☸", "good luck and karma", "Wheel"),
    "The Magician": ("✹", "manifestation and resourcefulness", "Magician"),
    "The Empress": ("♕", "abundance and nurturing", "Empress"),
    "The Fool": ("◯", "new beginnings and spontaneous adventures", "Fool")
}

# Chinese Zodiac
CHINESE_ZODIAC = {
    0: ("Monkey", "clever and curious"),
    1: ("Rooster", "observant and hardworking"),
    2: ("Dog", "loyal and honest"),
    3: ("Pig", "generous and compassionate"),
    4: ("Rat", "quick-witted and resourceful"),
    5: ("Ox", "patient and reliable"),
    6: ("Tiger", "brave and confident"),
    7: ("Rabbit", "gentle and elegant"),
    8: ("Dragon", "confident and intelligent"),
    9: ("Snake", "wise and enigmatic"),
    10: ("Horse", "energetic and independent"),
    11: ("Goat", "calm and gentle")
}

# Zodiac signs
ZODIAC_SIGNS = {
    (3, 21, 4, 19): ("Aries", "fiery and passionate"),
    (4, 20, 5, 20): ("Taurus", "grounded and determined"),
    (5, 21, 6, 20): ("Gemini", "adaptable and communicative"),
    (6, 21, 7, 22): ("Cancer", "emotional and intuitive"),
    (7, 23, 8, 22): ("Leo", "confident and charismatic"),
    (8, 23, 9, 22): ("Virgo", "analytical and practical"),
    (9, 23, 10, 22): ("Libra", "balanced and harmonious"),
    (10, 23, 11, 21): ("Scorpio", "intense and transformative"),
    (11, 22, 12, 21): ("Sagittarius", "adventurous and optimistic"),
    (12, 22, 1, 19): ("Capricorn", "ambitious and disciplined"),
    (1, 20, 2, 18): ("Aquarius", "innovative and humanitarian"),
    (2, 19, 3, 20): ("Pisces", "compassionate and mystical")
}

# Fortune cookie messages
FORTUNE_COOKIES = [
    "The path you seek may not be the one you need.",
    "Sometimes the greatest wisdom comes from simply listening.",
    "Your journey has just begun, return when you are ready.",
    "The answers you seek lie within, not without.",
    "Patience is not just waiting, but how you act while waiting.",
    "The universe has a plan, but it requires your participation.",
    "Not all who wander are lost, some are simply exploring.",
    "Your greatest strength is also your greatest weakness."
]

def get_zodiac_sign(birth_date):
    """Get zodiac sign from birth date"""
    month = birth_date.month
    day = birth_date.day

    for (start_month, start_day, end_month, end_day), (sign, trait) in ZODIAC_SIGNS.items():
        if (month == start_month and day >= start_day) or (month == end_month and day <= end_day):
            return sign, trait
    return "Unknown", "mysterious"

def get_chinese_zodiac(birth_date):
    """Get Chinese zodiac from birth year"""
    year = birth_date.year
    zodiac_index = year % 12
    return CHINESE_ZODIAC[zodiac_index]

def generate_reading(topic, user_name, birth_date, tarot_card, dice_num, orb_color):
    """Generate a personalized reading using Barnum Effect"""
    zodiac_sign, zodiac_trait = get_zodiac_sign(birth_date)
    chinese_animal, chinese_trait = get_chinese_zodiac(birth_date)

    # Get tarot card meaning
    tarot_symbol, tarot_meaning, tarot_label = TAROT_CARDS[tarot_card]

    readings = {
        "Health": [
            f"Ah, {user_name}, the cards speak clearly. As a {zodiac_sign}, your {zodiac_trait} nature influences your physical well-being. ",
            f"The {tarot_card} card reveals that {tarot_meaning} is calling to you. Your body is trying to communicate something important. ",
            f"The cosmic dice shows {dice_num}, which in ancient numerology represents the {['foundation', 'balance', 'creativity', 'stability', 'change', 'harmony'][dice_num-1]} you need in your health journey. ",
            f"The {orb_color} orb that appeared to you is no coincidence - it represents the energy surrounding your vitality. ",
            f"As someone born in the Year of the {chinese_animal}, you possess {chinese_trait} qualities that can aid your healing. ",
            "I sense that you sometimes neglect your own needs in favor of others. Your body is asking for more attention. ",
            "There's a connection between your emotional state and physical symptoms that you haven't fully acknowledged. ",
            "Trust your intuition about what your body needs - you know more than you think you do."
        ],
        "Wealth": [
            f"Welcome, {user_name}. The spirits of prosperity are stirring around you. As a {zodiac_sign}, your {zodiac_trait} energy attracts certain financial opportunities. ",
            f"The {tarot_card} appeared for a reason - {tarot_meaning} is the key to unlocking your abundance. ",
            f"The cosmic dice revealed {dice_num}, a powerful number that signals {['new foundations', 'partnerships', 'expansion', 'hard work', 'unexpected changes', 'balance'][dice_num-1]} in your financial realm. ",
            f"The {orb_color} energy you released shows the current state of your material manifestations. ",
            f"Your Chinese zodiac, the {chinese_animal}, makes you {chinese_trait} - traits that can be leveraged for prosperity. ",
            "I see that you have untapped potential for generating income that you haven't fully explored. ",
            "There's an opportunity coming that may not look like what you expect - stay open and alert. ",
            "Your relationship with money is more emotional than practical - this is both your strength and your challenge."
        ],
        "Relationship": [
            f"Ah, matters of the heart, {user_name}. Being a {zodiac_sign}, you approach love with {zodiac_trait} intensity. ",
            f"The {tarot_card} card has chosen you, revealing that {tarot_meaning} is at the center of your romantic destiny. ",
            f"The dice speaks - {dice_num} represents {['new beginnings', 'union', 'joy', 'foundation', 'freedom', 'harmony'][dice_num-1]} in the language of love. ",
            f"The {orb_color} orb reflects the energy you're projecting in your relationships - pay attention to its message. ",
            f"As the {chinese_animal}, you are {chinese_trait}, which deeply influences how you connect with others. ",
            "I sense you sometimes hold back your true feelings, fearing vulnerability. But this protection also blocks deeper connection. ",
            "There's someone in your life who understands you better than you realize - you may be overlooking their significance. ",
            "The relationship you seek begins with the relationship you have with yourself. Self-love is not selfish, it's essential."
        ],
        "Empowerment": [
            f"Greetings, {user_name}. Your quest for empowerment has brought you here. As a {zodiac_sign}, {zodiac_trait} power flows through you. ",
            f"The {tarot_card} has revealed itself, showing that {tarot_meaning} is your path to personal sovereignty. ",
            f"The cosmic dice displays {dice_num} - in the ancient wisdom, this number embodies {['independence', 'choice', 'expression', 'structure', 'liberation', 'responsibility'][dice_num-1]}. ",
            f"The {orb_color} light you unveiled represents the strength already within you, waiting to be acknowledged. ",
            f"Born under the {chinese_animal}, you are naturally {chinese_trait} - embrace these qualities fully. ",
            "You possess abilities and talents that you've been minimizing or hiding from others, perhaps even from yourself. ",
            "I see that you sometimes seek validation from external sources, but your greatest power comes from self-recognition. ",
            "The challenges you've faced weren't meant to break you, but to reveal your unshakeable core. You are stronger than you know."
        ]
    }

    reading_parts = readings[topic]
    full_reading = "".join(reading_parts)

    return full_reading

# Main app header with vintage landing image
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("IMG-20251220-WA0000.jpg", use_container_width=True)

st.markdown('<div class="main-title">🔮 MISZTIKUS SZANA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">✨ Ancient Wisdom from the Mystic Realms ✨</div>', unsafe_allow_html=True)

# Token display
st.markdown(f'<div class="token-display">💰 Your Tokens: {st.session_state.tokens} 💰</div>', unsafe_allow_html=True)

# Sidebar for token purchase and games
with st.sidebar:
    st.markdown("### 💰 Token Shop")
    st.markdown("Purchase tokens to unlock readings")
    st.markdown("**$1 per token**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Buy 5 Tokens"):
            st.session_state.tokens += 5
            st.success("5 tokens added!")
            st.rerun()
    with col2:
        if st.button("Buy 10 Tokens"):
            st.session_state.tokens += 10
            st.success("10 tokens added!")
            st.rerun()

    st.markdown("---")
    st.markdown("### 🎮 Earn Free Tokens")

    if st.button("🐱 Feed My Cat"):
        st.session_state.stage = 'feed_cat'
        st.rerun()

    if st.button("👥 Refer a Friend"):
        st.session_state.stage = 'refer_friend'
        st.rerun()

    if st.session_state.stage in ['welcome', 'main_menu', 'reading_complete']:
        if st.button("🏠 Return to Main"):
            st.session_state.stage = 'welcome'
            st.session_state.session_readings = 0
            st.rerun()

# Welcome stage
if st.session_state.stage == 'welcome':
    st.markdown("""
    <div class="szana-speech">
        "Hello, I'm glad you're here. I'm going to take a moment to tune into your energy..."
        <br><br>
        <i>*The crystal ball glows with ethereal light*</i>
        <br><br>
        "Now, are you prepared to hear insights that might challenge your current perspective?"
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("✨ Yes, I'm Ready", use_container_width=True):
            st.session_state.stage = 'choose_topic'
            st.rerun()

    with col3:
        if st.button("🥠 No, Just a Fortune Cookie", use_container_width=True):
            st.session_state.stage = 'fortune_cookie'
            st.rerun()

# Fortune cookie stage
elif st.session_state.stage == 'fortune_cookie':
    fortune = random.choice(FORTUNE_COOKIES)
    st.markdown(f"""
    <div class="fortune-cookie">
        <h3>🥠 Your Fortune Cookie 🥠</h3>
        <p><i>"{fortune}"</i></p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Return to Beginning"):
        st.session_state.stage = 'welcome'
        st.rerun()

# Choose topic stage
elif st.session_state.stage == 'choose_topic':
    st.markdown("""
    <div class="szana-speech">
        "Excellent. Your courage will be rewarded with truth."
        <br><br>
        "What brings you here today? What would you like insights on?"
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image("IMG-20251220-WA0001.jpg", use_container_width=True)
        if st.button("Select Health", key="health_btn", use_container_width=True):
            st.session_state.selected_topic = 'Health'
            st.session_state.stage = 'get_info'
            st.rerun()

    with col2:
        st.image("IMG-20251220-WA0002.jpg", use_container_width=True)
        if st.button("Select Wealth", key="wealth_btn", use_container_width=True):
            st.session_state.selected_topic = 'Wealth'
            st.session_state.stage = 'get_info'
            st.rerun()

    with col3:
        st.image("IMG-20251220-WA0003.jpg", use_container_width=True)
        if st.button("Select Relationship", key="relationship_btn", use_container_width=True):
            st.session_state.selected_topic = 'Relationship'
            st.session_state.stage = 'get_info'
            st.rerun()

    with col4:
        st.image("IMG-20251220-WA0004.jpg", use_container_width=True)
        if st.button("Select Empowerment", key="empowerment_btn", use_container_width=True):
            st.session_state.selected_topic = 'Empowerment'
            st.session_state.stage = 'get_info'
            st.rerun()

# Get user info stage
elif st.session_state.stage == 'get_info':
    st.markdown(f"""
    <div class="szana-speech">
        "Ah, you seek guidance on <b>{st.session_state.selected_topic}</b>. The spirits are listening."
        <br><br>
        "To channel the cosmic energies properly, I must know your name and birth date."
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input("Your Name:", key="name_input")
    birth_date = st.date_input("Your Date of Birth:",
                                min_value=datetime(1920, 1, 1),
                                max_value=datetime.now(),
                                value=datetime(1990, 1, 1))

    if st.button("Continue to Reading") and name:
        if st.session_state.tokens < 1:
            st.error("You need at least 1 token to proceed. Please purchase tokens from the sidebar.")
        else:
            st.session_state.user_name = name
            st.session_state.birth_date = birth_date
            st.session_state.stage = 'tarot'
            st.rerun()

# Tarot card selection
elif st.session_state.stage == 'tarot':
    st.markdown("""
    <div class="szana-speech">
        "Now, quiet your mind and let your intuition guide you..."
        <br><br>
        "Choose a card from my ancient Tarot deck. Trust your instincts."
    </div>
    """, unsafe_allow_html=True)

    # Display tarot cards in grid using actual card images
    cards = list(TAROT_CARDS.keys())

    # CSS to remove button padding and make cards clickable
    st.markdown("""
    <style>
    .tarot-container {
        cursor: pointer;
        transition: transform 0.2s;
    }
    .tarot-container:hover {
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

    # Display 6 rows of 4 cards each
    for row in range(6):
        cols = st.columns(4, gap="small")
        for col_idx in range(4):
            card_idx = row * 4 + col_idx
            if card_idx < len(cards):
                card_name = cards[card_idx]
                with cols[col_idx]:
                    # Display card image
                    st.image(f"tarot_card_{card_idx+1:02d}.png", use_container_width=True)
                    # Compact button directly below
                    if st.button("▲ Select", key=f"card_{card_idx}", use_container_width=True):
                        st.session_state.selected_card = card_name
                        st.session_state.tarot_selected = True
                        st.session_state.stage = 'dice'
                        st.rerun()

# Cosmic dice stage
elif st.session_state.stage == 'dice':
    st.markdown(f"""
    <div class="szana-speech">
        "You have chosen... The {st.session_state.selected_card}. Interesting..."
        <br><br>
        "Now, spin the cosmic dice. Let fate decide your path."
    </div>
    """, unsafe_allow_html=True)

    # Cosmic dice image with transparent background
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("cosmic_dice.png", use_container_width=True)

    if st.button("🌟 Spin the Cosmic Dice", use_container_width=True):
        st.session_state.dice_result = random.randint(1, 6)
        st.session_state.dice_rolled = True
        st.session_state.stage = 'orb'
        st.rerun()

# Cosmic orb stage
elif st.session_state.stage == 'orb':
    st.markdown(f"""
    <div class="szana-speech">
        "The dice has spoken... {st.session_state.dice_result}. The number of {['foundation', 'balance', 'creativity', 'stability', 'change', 'harmony'][st.session_state.dice_result-1]}."
        <br><br>
        "One final test... Burst the cosmic orb to release its energy!"
    </div>
    """, unsafe_allow_html=True)

    # Double-sized cosmic orb - centered
    st.markdown("""
    <div style='
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 40px 0;
    '>
        <div style='
            background: radial-gradient(circle, rgba(138, 43, 226, 0.4), rgba(75, 0, 130, 0.2));
            border-radius: 50%;
            padding: 40px;
            box-shadow: 0 0 60px rgba(138, 43, 226, 0.8), 0 0 100px rgba(75, 0, 130, 0.5);
            animation: pulse 2s infinite;
            display: flex;
            justify-content: center;
            align-items: center;
        '>
            <div style='font-size: 12em; text-shadow: 0 0 30px rgba(138, 43, 226, 0.8);'>🔮</div>
        </div>
    </div>
    <style>
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
    </style>
    """, unsafe_allow_html=True)

    if st.button("💫 Burst the Cosmic Orb", use_container_width=True):
        colors = ["violet", "indigo", "azure", "golden", "crimson", "emerald"]
        st.session_state.orb_result = random.choice(colors)
        st.session_state.orb_burst = True
        st.session_state.stage = 'generate_reading'
        st.rerun()

# Generate and display reading
elif st.session_state.stage == 'generate_reading':
    # Deduct token
    st.session_state.tokens -= 1
    st.session_state.session_readings += 1

    # Check for bonus token
    if st.session_state.session_readings == 3:
        st.session_state.tokens += 1
        st.balloons()
        st.success("🎉 You've completed 3 readings! Bonus token awarded!")

    reading = generate_reading(
        st.session_state.selected_topic,
        st.session_state.user_name,
        st.session_state.birth_date,
        st.session_state.selected_card,
        st.session_state.dice_result,
        st.session_state.orb_result
    )

    st.markdown(f"""
    <div class="szana-speech">
        "Ahhhh... The {st.session_state.orb_result} light emerges! The veil between worlds grows thin..."
        <br><br>
        "I can see clearly now. Let me share what the spirits reveal..."
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="reading-box">
        <h3 style="color: #ffd700; text-align: center;">✨ Your {st.session_state.selected_topic} Reading ✨</h3>
        <br>
        {reading}
        <br><br>
        <i style="color: #d4af37;">- Misztikus Szana</i>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.stage = 'reading_complete'

    # Reset reading variables
    st.session_state.tarot_selected = False
    st.session_state.dice_rolled = False
    st.session_state.orb_burst = False

    if st.button("Get Another Reading"):
        st.session_state.stage = 'choose_topic'
        st.rerun()

# Reading complete
elif st.session_state.stage == 'reading_complete':
    if st.button("Seek Another Reading"):
        st.session_state.stage = 'choose_topic'
        st.rerun()

# Feed the cat game
elif st.session_state.stage == 'feed_cat':
    st.markdown('<div class="main-title">🐱 Feed Szana\'s Cat 🐱</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="szana-speech">
        "Ah, how kind of you! My mystical cat, Shadow, is always hungry."
        <br><br>
        "Click on the correct treat to feed Shadow and earn a free token!"
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='text-align: center; font-size: 8em;'>🐈‍⬛</div>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #ffd700;'>Which treat does Shadow want?</h3>", unsafe_allow_html=True)

    correct = random.randint(0, 2)
    treats = ["🐟", "🥩", "🧀"]

    cols = st.columns(3)
    for idx, treat in enumerate(treats):
        with cols[idx]:
            if st.button(treat, key=f"treat_{idx}", use_container_width=True):
                if idx == correct:
                    st.session_state.tokens += 1
                    st.success("🎉 Shadow loved it! You earned 1 token!")
                    st.balloons()
                else:
                    st.error("😿 Shadow wasn't interested. Try again tomorrow!")

                if st.button("Return to Main"):
                    st.session_state.stage = 'welcome'
                    st.rerun()

# Refer a friend
elif st.session_state.stage == 'refer_friend':
    st.markdown('<div class="main-title">👥 Refer a Friend 👥</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="szana-speech">
        "The more souls who seek wisdom, the stronger the cosmic connection grows!"
        <br><br>
        "Share your unique referral link and earn tokens when friends join."
    </div>
    """, unsafe_allow_html=True)

    referral_link = f"https://misztikus-szana.app/ref/{st.session_state.user_name if st.session_state.user_name else 'mystic'}"

    st.markdown(f"""
    <div class="reading-box">
        <h3 style="color: #ffd700; text-align: center;">Your Referral Link</h3>
        <p style="text-align: center; font-size: 1.2em; word-break: break-all;">{referral_link}</p>
        <br>
        <p style="text-align: center;">Share this link to earn <b>2 tokens</b> per referral!</p>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input("Friend's Email (Demo - this adds a token immediately):")

    if st.button("Send Invitation") and email:
        st.session_state.tokens += 2
        st.success(f"Invitation sent to {email}! You earned 2 tokens!")
        st.balloons()

    if st.button("Return to Main"):
        st.session_state.stage = 'welcome'
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #d4af37; font-family: Cinzel, serif;'>
    <p>✨ Misztikus Szana - Ancient Wisdom for Modern Souls ✨</p>
    <p style='font-size: 0.8em;'>For entertainment purposes only</p>
</div>
""", unsafe_allow_html=True)
