import discord
import asyncio
import os
import random
from datetime import datetime, time, timedelta
import pytz
from flask import Flask, jsonify
import threading

# Bot Configuration
CHANNEL_ID = 1158472190052806721  # Deine Channel ID
DAILY_TIME = time(6, 0)  # 6:00 Uhr morgens
TIMEZONE = pytz.timezone('Europe/Berlin')  # Deutsche Zeitzone

# 50 verschiedene CaCo Nachrichten
DAILY_MESSAGES = [
    # Motivierende Texte für CaCo
    "🚀 Guten Morgen CaCo! Heute ist ein perfekter Tag, um eure Träume zu verwirklichen!",
    "💪 Hey CaCo! Jeder neue Tag ist eine neue Chance, großartig zu sein!",
    "⭐ Morgen CaCo Family! Ihr seid stärker als ihr denkt - zeigt es heute!",
    "🎯 Guten Morgen CaCo! Fokussiert euch auf eure Ziele und macht sie wahr!",
    "🌟 Hey CaCo! Heute ist euer Tag - nutzt jede Minute davon!",
    "🔥 Morgen CaCo Warriors! Lasst euer inneres Feuer heute brennen!",
    "💎 Guten Morgen CaCo! Ihr seid wie Diamanten - unter Druck entstehen die schönsten!",
    "🏆 Hey CaCo Champions! Heute wird ein Siegertag - ich spüre es!",
    "🌈 Morgen CaCo! Nach jedem Sturm kommt ein Regenbogen - heute scheint eure Sonne!",
    "⚡ Guten Morgen CaCo Energy! Ladet eure Batterien auf und rockt den Tag!",
    
    # Positive Texte
    "😊 Guten Morgen! Ein Lächeln ist der beste Start in den Tag!",
    "🌸 Morgen zusammen! Jeder Tag bringt neue Möglichkeiten mit sich!",
    "✨ Hey! Heute ist ein magischer Tag - macht das Beste daraus!",
    "🌻 Guten Morgen! Blüht heute wie die schönsten Sonnenblumen!",
    "🦋 Morgen! Verwandelt euch heute wie ein wunderschöner Schmetterling!",
    "🌅 Guten Morgen! Ein neuer Sonnenaufgang, ein neues Abenteuer!",
    "💫 Hey! Ihr seid die Sterne eures eigenen Himmels!",
    "🎨 Morgen Künstler! Malt euer Leben heute in den schönsten Farben!",
    "🌺 Guten Morgen! Lasst eure Seele heute wie eine Blume erblühen!",
    "🎵 Hey! Das Leben spielt heute eure Lieblingsmelodie!",
    
    # Gute Morgen Grüße
    "☀️ Guten Morgen! Die Sonne scheint für euch heute besonders hell!",
    "🐦 Morgen! Selbst die Vögel singen heute fröhlicher!",
    "🌤️ Guten Morgen! Ein wunderschöner Tag wartet auf euch!",
    "🌷 Morgen ihr Lieben! Startet sanft in diesen neuen Tag!",
    "☕ Guten Morgen! Zeit für den ersten Kaffee und gute Gedanken!",
    "🌄 Morgen! Die Berge grüßen euch mit einem neuen Tagesanfang!",
    "🌊 Guten Morgen! Lasst euch von der Ruhe des Morgens inspirieren!",
    "🍃 Morgen! Atmet tief durch und spürt die frische Morgenluft!",
    "🌞 Guten Morgen Sonnenscheine! Ihr erhellt jeden Raum!",
    "🦅 Morgen! Fliegt heute hoch wie die Adler am Himmel!",
    
    # Mehr motivierende CaCo Texte
    "🎪 Guten Morgen CaCo Zirkus! Heute seid ihr die Stars der Manege!",
    "🚂 Morgen CaCo Express! Alle einsteigen zum Erfolg!",
    "🎮 Hey CaCo Gamer! Today you level up in real life!",
    "🏰 Guten Morgen CaCo Kingdom! Heute regiert ihr euer Schicksal!",
    "🎭 Morgen CaCo Theater! Heute spielt ihr die Hauptrolle!",
    "🎪 Hey CaCo Family! Zusammen sind wir unschlagbar!",
    "🚀 Guten Morgen CaCo Space! Heute fliegt ihr zu den Sternen!",
    "⚔️ Morgen CaCo Warriors! Heute kämpft ihr für eure Träume!",
    "🎨 Hey CaCo Artists! Heute malt ihr euer Meisterwerk!",
    "🎯 Guten Morgen CaCo Snipers! Zielt heute auf eure Ziele!",
    
    # Weitere positive Vibes
    "🌈 Morgen Regenbogen-Seelen! Bringt heute Farbe ins Leben!",
    "🎈 Guten Morgen! Lasst eure Träume heute wie Ballons steigen!",
    "🎁 Morgen! Jeder neue Tag ist ein Geschenk - packt es aus!",
    "🎊 Hey! Heute gibt es Grund zu feiern - ihr lebt!",
    "🌟 Guten Morgen Sterne! Ihr leuchtet heller als ihr denkt!",
    "🎵 Morgen Musikanten! Heute komponiert ihr eure Erfolgsmelodie!",
    "🎪 Hey Zauberer! Heute macht ihr Unmögliches möglich!",
    "🌸 Guten Morgen Blüten! Heute entfaltet ihr eure volle Pracht!",
    "🦋 Morgen Verwandlungskünstler! Heute werdet ihr zu dem, was ihr sein wollt!",
    "⭐ Hey Wunscherfüller! Heute gehen eure Träume in Erfüllung!",
    
    # Finale motivierende Nachrichten
    "🔑 Guten Morgen Schlüssel-Finder! Heute öffnet ihr alle Türen!",
    "🌅 Morgen Sonnenaufgangs-Zeugen! Ihr startet perfekt in den Tag!",
    "💝 Hey Geschenke! Ihr seid das beste Geschenk für diese Welt!",
    "🎯 Guten Morgen Ziel-Erreicher! Heute trefft ihr ins Schwarze!",
    "🌊 Morgen Wellen-Reiter! Surft heute auf der Erfolgswelle!"
]

# Discord Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

def get_daily_message():
    """Wählt eine zufällige Nachricht aus den 50 CaCo Texten"""
    return random.choice(DAILY_MESSAGES)

async def send_daily_message():
    """Sendet die tägliche CaCo Nachricht"""
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if not channel:
            print(f"❌ Channel mit ID {CHANNEL_ID} nicht gefunden!")
            return
        
        message = get_daily_message()
        await channel.send(message)
        
        now = datetime.now(TIMEZONE)
        print(f"✅ Tägliche CaCo-Nachricht gesendet: {now.strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"📝 Gesendete Nachricht: \"{message}\"")
        
    except Exception as e:
        print(f"❌ Fehler beim Senden der Nachricht: {e}")

async def daily_scheduler():
    """Täglich um 6 Uhr eine Nachricht senden - KORRIGIERTE VERSION"""
    while True:
        try:
            now = datetime.now(TIMEZONE)
            target_time = TIMEZONE.localize(datetime.combine(now.date(), DAILY_TIME))
            
            # Wenn die Zeit schon vorbei ist, für den nächsten Tag planen
            if now >= target_time:
                target_time = target_time + timedelta(days=1)
            
            # Berechne Wartezeit bis zur nächsten Nachricht
            wait_seconds = (target_time - now).total_seconds()
            
            print(f"⏰ Nächste CaCo-Nachricht: {target_time.strftime('%d.%m.%Y um %H:%M:%S')}")
            print(f"⏳ Warte {wait_seconds/3600:.1f} Stunden...")
            
            await asyncio.sleep(wait_seconds)
            await send_daily_message()
            
        except Exception as e:
            print(f"❌ Scheduler Fehler: {e}")
            await asyncio.sleep(3600)  # Bei Fehler 1 Stunde warten

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")
    print(f"📅 Tägliche CaCo-Nachricht geplant für {DAILY_TIME.strftime('%H:%M')} Uhr (Deutsche Zeit)")
    print(f"📍 Ziel-Channel ID: {CHANNEL_ID}")
    print(f"📝 {len(DAILY_MESSAGES)} verschiedene Nachrichten verfügbar")
    
    # Starte den täglichen Scheduler
    asyncio.create_task(daily_scheduler())

@bot.event
async def on_message(message):
    """Test Command für sofortiges Testen - MIT DEBUG"""
    print(f"📨 Nachricht empfangen: '{message.content}' von {message.author}")
    
    if message.author == bot.user:
        print("🤖 Eigene Nachricht ignoriert")
        return
    
    # Test Command: !test oder !caco
    if message.content.lower() in ['!test', '!caco', '!testmessage']:
        print("🎯 Test-Command erkannt! Sende Nachricht...")
        try:
            await send_daily_message()
            await message.channel.send("✅ Test-Nachricht wurde gesendet!")
            print("✅ Test erfolgreich!")
        except Exception as e:
            print(f"❌ Fehler beim Test: {e}")
            await message.channel.send(f"❌ Fehler: {e}")

# Flask Server für Health Check und UptimeRobot
app = Flask(__name__)

@app.route('/')
def health_check():
    """Health Check für Render"""
    bot_status = "online" if bot.user else "offline"
    uptime = 0  # Hier könntest du die tatsächliche Uptime berechnen
    
    return jsonify({
        "status": bot_status,
        "bot": str(bot.user) if bot.user else "nicht verbunden",
        "uptime": uptime,
        "nextMessage": f"Täglich um {DAILY_TIME.strftime('%H:%M')} Uhr",
        "messagesAvailable": len(DAILY_MESSAGES),
        "timezone": str(TIMEZONE)
    })

@app.route('/ping')
def ping():
    """Ping endpoint für UptimeRobot (alle 5 Minuten)"""
    return "pong", 200

def run_flask():
    """Startet Flask Server in separatem Thread"""
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=False)

# Starte Flask Server in eigenem Thread
if __name__ == "__main__":
    # Flask Server starten
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print(f"🌐 Health check server läuft auf Port {os.environ.get('PORT', 3000)}")
    print(f"📡 UptimeRobot kann /ping alle 5 Minuten aufrufen")
    
    # Discord Bot starten
    token = os.environ.get('DISCORD_TOKEN')
    if not token:
        print("❌ DISCORD_TOKEN Environment Variable nicht gesetzt!")
        exit(1)
    
    try:
        bot.run(token)
    except Exception as e:
        print(f"❌ Fehler beim Starten des Bots: {e}")
