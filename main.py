from cfg import crops
import json, random, threading, time

defaultdata = {
"name": "", 
"money": 10.0, 
"multiplier": 1.0, 
"xp": 0, 
"farmslots": 1, 
"autosell": "true",
"cooldown": 3.0,
"farms": {"apple": 0, "mango": 0}, 
"crops": {}
}

ver = '0.3.2-a'
pdata = None

try:
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  print(f'''
antfrm {ver}
Welcome back {pdata['name']}''')
except FileNotFoundError:
    pdata = defaultdata
    pdata['name'] = input(f'''antfrm {ver}
Input Name

> ''')
    with open('pdata.json', 'w') as f:
      json.dump(pdata, f)
  
def help(args):
  print(f'''Commands:
  h - Shows this menu
  x - Exit game
  p - Shows your profile
  f - Harvest crops
  b - Buy farms (b [crop] [amount])
  s - Sells all crops
  m - Opens shop menu (WIP)

Options:
 ~n - Change your name
 ~a - Toggle Autosell
 ~r - Reset game''')

def quit(args):
  print("Goodbye\n")
  exit()
  
def stats(args):
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  print(f'''{pdata['name']}'s Profile:
  Money: {pdata['money']}
  Multiplier: {pdata['multiplier']}x
  Farm Slots: {pdata['farmslots']}''')

def namechange(args):
  newn = input(f'''New Name: (Leave blank for no change)
  
~ ''')
  if newn != '':
    pdata['name'] = newn
    with open('pdata.json', 'w') as f:
      json.dump(pdata, f)
    print('')
  else:
    print('Name not changed')
  
def reset(args):
  ans = input(f'''Are you sure you want to reset? (y/N)
  
~ ''')
  if ans.lower() == "y":
    pdata = defaultdata
    pdata['name'] = input(f'''antfrm {ver}
Input Name

> ''')
    with open('pdata.json', 'w') as f:
      json.dump(pdata, f)
  else:
    print("Reset cancelled")

def buy(args):
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  try:
    clist = list(pdata['crops'].keys()).remove(args[0])
  except ValueError:
    clist = list(pdata['crops'].keys())
  if clist == None:
    clist = 0
  else:
    clist = len(clist)
  if args == []:
    print('Type "s" for shop')
  elif args[0] in pdata['farms']:
    try:
      amt = int(args[1])
    except:
      amt = 1
    if pdata['money'] >= crops[args[0]]['buy-price'] * amt:
      if pdata['farmslots'] > clist:
        pdata['farms'][args[0]] += amt
        pdata['money'] -= crops[args[0]]['buy-price'] * amt
        with open('pdata.json', 'w') as f:
          json.dump(pdata, f)
        print(f'''Bought {amt}x {args[0]} farm (-${crops[args[0]]['buy-price'] * amt})''')
      else:
        print('No available farm slots.\n')
    else:
      print(f'''Not enough money, you need ${crops[args[0]]['buy-price']*amt - pdata['money']} more.''')
  else:
    print('Type "s" for shop')

def sell(args):
  if pdata['crops'].values() != 0:
    for crop, count in pdata['crops'].items():
      sellamt =+ pdata['crops'][crop] * crops[crop]['sell-price']
      print(sellamt)
    pdata['money'] = pdata['money'] + sellamt
    print(f'''Sold all for ${sellamt}''')
  else:
    print('a')
  with open('pdata.json', 'w') as f:
    json.dump(pdata, f)

def shop(args):
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  print("to do: market")

t1 = 0
def harvest(args):
  global t1
  t0 = time.time()
  tdel = round(t0-t1, 1)
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  if sum(pdata['farms'].values()) == 0:
    print("You have no farms. Buy some from the market")
  elif tdel >= pdata['cooldown']:
    totals = {}
    sellamt = 0
    print("Your ants collected:")
    for farm, count in pdata['farms'].items():
      totals[farm] = int(round(count * crops[farm]['yield'] * random.uniform(1,2.5),0)) #yield
      try:
        pdata['crops'][farm] += totals[farm]
      except:
        pdata['crops'] = pdata['crops'] | totals
      if totals[farm] > 0:
        print(f''' +{totals[farm]} {farm}''')
      if pdata['autosell'] == "true":
        sellamt += totals[farm] * crops[farm]['sell-price']
        pdata['crops'][farm] -= count
        pdata['money'] += sellamt
      t1 = time.time()
    with open('pdata.json', 'w') as f:
      json.dump(pdata, f)
    if sellamt != 0:
      print(f''' Sold all for ${sellamt}''')
    else:
      print('')
  else:
    print(f'''Please wait {round(pdata['cooldown'] - tdel, 1)} more seconds''')

def togglesell(args):
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  if pdata['autosell'] == "true":
    pdata['autosell'] = "false"
    print("Autosell toggled off")
    with open('pdata.json', 'w') as f:
      json.dump(pdata, f)
  elif pdata['autosell'] == "false":
    pdata['autosell'] = "true"
    print("Autosell toggled on")
    with open('pdata.json', 'w') as f:
      json.dump(pdata, f)
    
def invalid_command(args):
  print('Type "h" for help')

commands = {
  'h': help,
  'x': quit,
  'p': stats,
  'f': harvest,
  'b': buy,
  's': sell,
  'm': shop,
  '~n': namechange,
  '~r': reset,
  '~a': togglesell,
}

while True:
  inp = input('\n> ').split(' ')
  commands.get(inp[0], invalid_command)(inp[1:])