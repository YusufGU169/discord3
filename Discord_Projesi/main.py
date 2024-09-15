import discord
from discord.ext import commands
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
from random import *
from modelim import *
from banaait import *
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')
@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)
@bot.command()
async def kontrol(ctx):
    if ctx.message.attachments:
        for resim in ctx.message.attachments:
            resim_ismi = resim.filename
            resim_url = resim.url
            await resim.save(f"./{resim.filename}")
            await ctx.send(f"Resim kaydedildi./{resim.filename}")
            await ctx.send(guse1(model2="keras_model1.h5",labels2="labels1.txt", image2=f"./{resim.filename}"))
    else:
        await ctx.send("Fotoğraf eklemeyi unuttunuz.")
@bot.command()
async def piknikalani(ctx):
    dagcevap = ["Herhalde dağın yakınlarındasın, dağın kenarına kurabilirsin.", "Dağın kenarında boş alan var, oraya kurabilirsin!", "Dağdasın, dağda boş alan varsa oraya kurabilirsin, çok eğimli değilse. Eğer çok eğimliyse kenarına kurabilirsin."]
    ovacevap = ["Heryer bomboş istediğin yere kur!", "Dümdüz ve bomboş, istediğin yere kurabilirsin. Eğer ağaç varsa gölgelik olarak ağacın altında piknik kurabilirsin!", "Ağacın altında kurabilirsin, rahat olur."]
    pacevap = ["Piknik masasına kurabilirsin!", "Yere kurabilirsin! Mangal kurabileceğin bir yer varsa oraya kur.", "Piknik masasına kurabilirsin! Olmazsa yere kurabilirsin!"]
    ormancevap = ["Şu anda bir ormandasın. Mangal kuracaksan dikkatli ol, yangın çıkarabilirsin!!!", "Ormandasın, ağaçların arasında geniş ve boş bir alan varsa oraya kurabilirsin.", "Mangal kurmadan önce geniş ve boş bir alan bul, oraya dikkatlice kur. Yangın çıkartma!"]  
    taninmayannesnecevap = "Üzgünüm, resimde neyin gösterildiğinden emin değilim."
    if ctx.message.attachments:
        for piknikresim in ctx.message.attachments:
            pr_ismi = piknikresim.filename
            pr_url = piknikresim.url
            await piknikresim.save(f"./{piknikresim.filename}")
            # Disable scientific notation for clarity
            np.set_printoptions(suppress=True)
            # Load the model
            model = load_model("keras_model1.h5", compile=False)
            # Load the labels
            class_names = open("labels1.txt", "r").readlines()
            # Create the array of the right shape to feed into the keras model
            # The 'length' or number of images you can put into the array is
            # determined by the first position in the shape tuple, in this case 1
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            # Replace this with the path to your image
            image = Image.open(pr_ismi).convert("RGB")
            # resizing the image to be at least 224x224 and then cropping from the center
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
            # turnthe image into a numpy array
            image_array = np.asarray(image)
            # Normalize the image
            normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
            # Load the image into the array
            data[0] = normalized_image_array
            # Predicts the model
            prediction = model.predict(data)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]
            secilen_sinif = class_name[2:]
            if secilen_sinif == "Dağ\n":
                cwrite = (dagcevap[randint(0,2)])
            elif secilen_sinif == "Ova / Çayır\n":
                cwrite = (ovacevap[randint(0,2)])
            elif secilen_sinif == "Piknik Alanları\n":
                cwrite = (pacevap[randint(0,2)])
            elif secilen_sinif == "Orman\n":
                cwrite = (ormancevap[randint(0,2)])
            elif secilen_sinif == "Yabanci Nesne\n":
                cwrite = ("Üzgünüm, resimde neyin gösterildiğinden emin değilim.")
        await ctx.send(cwrite)
    else:
        await ctx.send("Fotoğraf eklemeyi unuttunuz.")
bot.run(jetonum)