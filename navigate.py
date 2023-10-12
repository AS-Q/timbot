# Основано на https://github.com/PrismarineJS/mineflayer/blob/master/docs/mineflayer.ipynb
# Документация тут https://github.com/PrismarineJS/mineflayer/blob/master/docs/ru/README_RU.md
# Описание API тут https://github.com/PrismarineJS/mineflayer/blob/master/docs/ru/api_ru.md
# API на JS. Это похоже на C++, только попроще. Надо перекладывать на питон по этому образцу

# Тест: Подключение и отображение


from javascript import require, On, Once, AsyncTask, once, off
mineflayer = require('mineflayer')
mfviewer = require('prismarine-viewer').mineflayer
pathfinder = require('mineflayer-pathfinder')

# Создаём бота со случайным именем (тут лучше вписать чёньть  постоянное)
random_number = id([]) % 1000 # Give us a random number upto 1000
BOT_USERNAME = f'colab_{random_number}'
# в список параметров можно добавить 'password'
bot = mineflayer.createBot({ 'host': 'pjs.deptofcraft.com', 'port': 25565, 'username': BOT_USERNAME, 'hideErrors': False })

# Действия при появлении в игре

# @On - это обёртка события для коннектора к JS. Пишешь так перед любой функцией и она будет срабатывать по этому событию
# @Once - то же самое, только однократно, а не по каждому
@Once(bot, 'spawn')
def on_spawn(this):
    #bot.chat('I spawned')
    print('username:', BOT_USERNAME, 'pos:', this.entity.position)
    mfviewer(this, { 'port': 3000 })
    # как тут отпишется, зайти на https://localhost:3000
    
    # когда будет идти, будет за собой путь рисовать
    path = [this.entity.position.clone()]

    @On(this, 'move')
    def on_move(this, t):
        #print('t:',t)
        if (path[len(path) - 1].distanceTo(this.entity.position) > 1):
            path.append(this.entity.position.clone())
            this.viewer.drawLine('path', path)

nonce = input('Press any key')

# Инициализируем навигацию

bot.loadPlugin(pathfinder.pathfinder)
# Create a new minecraft-data instance with the bot's version
mcData = require('minecraft-data')(bot.version)
# Create a new movements class
movements = pathfinder.Movements(bot, mcData)
# How far to be fromt the goal
RANGE_GOAL = 1

bot.removeAllListeners('chat')
@On(bot, 'chat')
def handleMsg(this, sender, message, *args):
  if sender and (sender != BOT_USERNAME):
    bot.chat('Hi, you said ' + message)
    if 'come' in message:
      player = bot.players[sender]
      target = player.entity
      if not target:
        bot.chat("I don't see you !")
        return
      pos = target.position
      bot.pathfinder.setMovements(movements)
      bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, RANGE_GOAL))
    if 'stop' in message:
      off(bot, 'chat', handleMsg)


# тестируем навигацию без чата
# будет куда-то бестолково идти, гибнуть и респавниться
pos = bot.entity.position
bot.pathfinder.setMovements(movements)
bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x-10, pos.y+20, pos.z, RANGE_GOAL))
