from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime
import random
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

# DB Connect
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sugarpanda",
    database="neurooracle"
)
cursor = db.cursor()

# Helper: normalize mood string to base keyword
def clean_mood(raw):
    m = raw.lower()
    if 'angry' in m:
        return 'angry'
    if 'anxious' in m:
        return 'anxious'
    if 'fearful' in m:
        return 'fearful'
    if 'sad' in m:
        return 'sad'
    if 'excited' in m:
        return 'excited'
    if 'happy' in m:
        return 'happy'
    if 'surprised' in m:
        return 'surprised'
    if 'disgusted' in m:
        return 'disgusted'
    if 'neutral' in m:
        return 'neutral'
    return 'neutral'

# Numeric mapping for plotting
mood_map = {
    "angry": 1,
    "anxious": 2,
    "fearful": 2,
    "sad": 3,
    "neutral": 4,
    "surprised": 4,
    "excited": 5,
    "happy": 6,
    "disgusted": 2
}

# Reverse for ticks
inverse_mood_map = {v: k.capitalize() for k, v in mood_map.items() if k in ["angry", "anxious", "sad", "neutral", "excited", "happy"]}

# Color palette
palette = {
    'happy': '#22c55e',
    'excited': '#f59e0b',
    'neutral': '#64748b',
    'sad': '#6366f1',
    'anxious': '#fb7185',
    'angry': '#ef4444',
    'fearful': '#f97316',
    'surprised': '#0ea5e9',
    'disgusted': '#a855f7'
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/log_mood", methods=["POST"])
def log_mood():
    data = request.get_json()
    mood = data.get("mood")
    day = data.get("day", "")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = "INSERT INTO mood_logs (mood, reflection, timestamp) VALUES (%s, %s, %s)"
    cursor.execute(query, (mood, day, timestamp))
    db.commit()
    return jsonify({"message": "✅ Mood and reflection logged successfully."})

@app.route('/insight', methods=['POST'])
def get_insight():
    mood = request.json.get('mood', 'Neutral')

    mood_insights = {
        'Happy 😊': [
            "Happiness is contagious—spread it!",
            "Treasure the moments that make you smile.",
            "Let the joy of today inspire your tomorrow.",
            "Your light can brighten someone else's day.",
            "Joy multiplies when you share it."
        ],
        'Sad 😔': [
            "It's okay to feel sad. Let yourself heal.",
            "Tough days don’t define you.",
            "Emotions are valid. You're not alone.",
            "Dark clouds pass. Hold on.",
            "Every tear waters your inner strength."
        ],
        'Angry 😠': [
            "Anger is a signal—pause and understand it.",
            "Channel your anger into positive action.",
            "Take a deep breath. You’re in control.",
            "Frustration is temporary. Solutions are real.",
            "Express, don’t suppress—mindfully."
        ],
        'Neutral 😐': [
            "Every moment holds potential—notice it.",
            "Even calm days are part of the story.",
            "Balance is a beautiful space to be in.",
            "Neutrality offers a chance to reflect.",
            "Stillness is powerful in its own way."
        ],
        'Excited 🤩': [
            "Let your excitement fuel your dreams!",
            "This spark can light up everything you touch.",
            "Embrace the thrill—you're on a journey!",
            "Your energy is magnetic—use it well.",
            "Stay hyped, stay focused!"
        ],
        'Anxious 😰': [
            "Breathe. You’ve handled tough moments before.",
            "Anxiety comes and goes. You remain strong.",
            "Small steps forward matter.",
            "You’re not your thoughts—you’re so much more.",
            "Calmness is a skill you’re mastering."
        ],
         'Fearful 😨': [  
            "Fear is natural—courage is acting despite it.",
            "Your fear is valid, but it doesn’t own you.",
            "Lean into the discomfort—you grow there.",
            "Every brave soul has felt fear too.",
            "This moment will pass—breathe through it."
        ]
    }

    # Mood-based quotes
    mood_quotes = {
        'Happy 😊': [
            "😊 Spread sunshine wherever you go.",
            "🙂 A smile is the best makeup.",
            "🌞 Every day may not be good, but there’s something good in every day.",
            "💛 Laugh loud, love harder.",
            "🎉 Celebrate the little victories."
        ],
        'Sad 😔': [
            "💧 Sometimes, it's okay to just feel.",
            "🌧️ Rainy days help flowers grow.",
            "🖤 You are allowed to outgrow people who bring you down.",
            "🌙 Healing takes time, and that’s okay.",
            "🫂 Even broken hearts still beat."
        ],
        'Angry 😠': [
            "🔥 Anger is just pain looking for a voice.",
            "💢 Breathe before you react.",
            "🧠 Calm mind brings inner strength.",
            "🛑 Pause. Reflect. Respond.",
            "🕯️ Peace begins with you."
        ],
        'Neutral 😐': [
            "⚪ Balance is the key to everything.",
            "🌀 Sometimes, no feeling is a feeling too.",
            "🌫️ Drift and observe, don’t force it.",
            "📖 Life writes in both ink and erasers.",
            "🔁 Go with the flow, but don’t forget the paddle."
        ],
        'Excited 🤩': [
            "🚀 Let your enthusiasm lift you.",
            "⚡ Your spark could ignite the world.",
            "🎈 Feel the energy and let it guide you.",
            "🎯 Aim high, jump higher!",
            "🪩 Shine loud, shine proud!"
        ],
        'Anxious 😰': [
            "🫁 Inhale calm, exhale tension.",
            "🧘 You’ve survived 100% of your worst days.",
            "🌬️ Let go of what you can’t control.",
            "🧩 One step at a time is all it takes.",
            "🔒 It’s safe to take your time."
        ],
        'Fearful 😨': [  
            "🛡️ Courage doesn’t mean no fear, just action in spite of it.",
            "🌌 Feel the fear, do it anyway.",
            "🕯️ A little light defeats a lot of darkness.",
            "🏔️ Fear is a reaction. Bravery is a decision.",
            "🎭 Even the strongest wear masks sometimes."
        ]
    }

    selected_insight = random.choice(mood_insights.get(mood, ["Stay strong. You’re doing better than you think."]))
    selected_quote = random.choice(mood_quotes.get(mood, ["You’re worthy of good things."]))

    return jsonify({'insight': selected_insight, 'quote': selected_quote})

@app.route("/view_moods", methods=["GET"])
def view_moods():
    cursor.execute("SELECT mood, reflection, timestamp FROM mood_logs ORDER BY timestamp DESC LIMIT 10")
    moods = [{"mood": row[0], "day": row[1], "timestamp": row[2]} for row in cursor.fetchall()]
    return jsonify({"moods": moods})

# NEW: Mood graph JSON API for AJAX
@app.route("/mood-graph")
def mood_graph():
    cursor.execute("SELECT mood, reflection, timestamp FROM mood_logs ORDER BY timestamp DESC LIMIT 7")
    rows = list(reversed(cursor.fetchall()))
    if not rows:
        return render_template("mood_graph.html", graph_urls=None)

    timestamps = [
        r[2] if isinstance(r[2], datetime) else datetime.strptime(r[2], "%Y-%m-%d %H:%M:%S")
        for r in rows
    ]
    raw_moods = [r[0] for r in rows]
    cleaned = [clean_mood(m) for m in raw_moods]
    levels = [mood_map.get(m, mood_map['neutral']) for m in cleaned]
    labels = [ts.strftime('%d %b') for ts in timestamps]
    colors = [palette.get(m, '#64748b') for m in cleaned]

    os.makedirs('static/graphs', exist_ok=True)
    timestamp_suffix = datetime.now().strftime('%Y%m%d%H%M%S')

    # Line plot
    plt.figure(figsize=(10, 4))
    plt.plot(labels, levels, marker='o', linewidth=2)
    for i, (x, y) in enumerate(zip(labels, levels)):
        plt.scatter(x, y, s=100, color=colors[i], edgecolor='white', linewidth=1.2, zorder=3)
        plt.text(i, y + 0.15, cleaned[i].capitalize(), ha='center', va='bottom', fontsize=9, weight='bold')
    plt.title("Mood Trend - Last 7 Logs", fontsize=16)
    ticks = sorted({v for k, v in mood_map.items() if k in ['angry','anxious','sad','neutral','excited','happy']})
    plt.yticks(ticks, [inverse_mood_map[v] for v in ticks])
    plt.tight_layout()
    line_path = f"static/graphs/mood_line_{timestamp_suffix}.png"
    plt.savefig(line_path)
    plt.close()

    # Bar chart
    plt.figure(figsize=(10, 4))
    bars = plt.bar(labels, levels, color=colors, edgecolor='black')
    for bar, mood in zip(bars, cleaned):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1, mood.capitalize(), ha='center', fontsize=9)
    plt.title("Mood Bar Overview", fontsize=16)
    plt.ylim(0, max(mood_map.values()) + 1)
    plt.yticks(ticks, [inverse_mood_map[v] for v in ticks])
    plt.tight_layout()
    bar_path = f"static/graphs/mood_bar_{timestamp_suffix}.png"
    plt.savefig(bar_path)
    plt.close()

    # Smoothed average
    window = 3
    arr = np.array(levels, dtype=float)
    mov_avg = np.convolve(arr, np.ones(window)/window, mode='valid') if len(arr) >= window else arr
    x_labels_avg = labels[window - 1:] if len(arr) >= window else labels
    plt.figure(figsize=(10, 3))
    plt.fill_between(x_labels_avg, mov_avg, alpha=0.3)
    plt.plot(x_labels_avg, mov_avg, marker='o', linewidth=2)
    plt.title("Smoothed Mood (Moving Average)", fontsize=14)
    plt.tight_layout()
    smooth_path = f"static/graphs/mood_smooth_{timestamp_suffix}.png"
    plt.savefig(smooth_path)
    plt.close()

    graph_urls = {
        'line': '/' + line_path,
        'bar': '/' + bar_path,
        'smooth': '/' + smooth_path
    }
    return render_template("mood_graph.html", graph_urls=graph_urls)


if __name__ == "__main__":
    app.run(debug=True)
