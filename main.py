import shutil
import os
import configparser as cfp
from tqdm import tqdm
import sys

sysdrive = os.environ["SYSTEMDRIVE"]
user = os.getlogin()
cwd = os.getcwd()

def autodetect():
    if os.path.exists(f'{sysdrive}\\Users\\{user}\\AppData\\Local\\osu!'):
        return True
    else:
        return False

def outputpath():
    print('Set ur output path (default is the app folder, set it to blank to use the default)')
    output = input(f'(default is {cwd}): ')
    if output == '':
        outpath = cwd 
    elif os.path.exists(output):
        outpath = output
    else:
        print('Invalid output path!')
        outpath = outputpath()
    return outpath

if os.path.exists('config.ini'):
    config = cfp.ConfigParser()
    config.read('config.ini')
    osupath = config['path']['osupath']
    bmapdir = config['path']['beatmaps']
    skindir = config['path']['skins']
else:
    if autodetect():
        osupath = f'{sysdrive}\\Users\\{user}\\AppData\\Local\\osu!'
        bmapdir = f'{osupath}\\Songs'
        skindir = f'{osupath}\\Skins'
        outpath = outputpath()
        config = cfp.ConfigParser()
        config['path'] = {'osupath': osupath, 'beatmaps': bmapdir, 'skins': skindir, 'output': outpath}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        print('Could not find osu! installation, please specify the path manually')
        osupath = input('Enter the path to osu!: ')
        bmapdir = f'{osupath}\\Songs'
        skindir = f'{osupath}\\Skins'
        outpath = outputpath()
        config = cfp.ConfigParser()
        config['path'] = {'osupath': osupath, 'beatmaps': bmapdir, 'skins': skindir, 'output': outpath}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
bmap = os.listdir(bmapdir)
skin = os.listdir(skindir)
def homescr(messages=None):
    print('    Welcome to the osu! beatmaps and skins packer!')
    print('    This program will pack osu! beatmaps and skins folder into .osz or .osk files')
    print('  --------------------------------------------------------------')
    print('    Select the action you want to perform:')
    print('       1. Pack beatmaps and skins')
    print('       2. Pack beatmaps only')
    print('       3. Pack skins only')
    print('       4. Change output path')
    print('       5. Exit')
    print('  --------------------------------------------------------------')
    if messages:
        print(messages)

def bmappack(resultpath):
    for beatmap in tqdm(bmap, desc='Packing beatmaps', bar_format = '{l_bar}{bar}| {n_fmt}/{total_fmt} beatmaps (this might take a while)'):
        if os.path.isdir(f'{bmapdir}\\{beatmap}'):
            shutil.make_archive(f'{resultpath}\\{beatmap}', 'zip', f'{bmapdir}\\{beatmap}')
            os.rename(f'{resultpath}\\{beatmap}.zip', f'{resultpath}\\{beatmap}.osz')

def skinpack(resultpath):
    for skin2 in tqdm(skin, desc='Packing skins', bar_format = '{l_bar}{bar}| {n_fmt}/{total_fmt} skins (this might take a while)'):
        if os.path.isdir(f'{skindir}\\{skin2}'):
            shutil.make_archive(f'{resultpath}\\{skin2}', 'zip', f'{skindir}\\{skin2}')
            os.rename(f'{resultpath}\\{skin2}.zip', f'{resultpath}\\{skin2}.osk')

def packagain():
    print('Are u wanna pack beatmaps and skins again? (y/n)')
    sure = input('(choose y or n): ')
    if sure == 'y':
        os.system('cls')
        menu()
    else:
        print('Bye!')
        exit()

def menu(message=None):
    os.system('cls')
    if message:
        homescr(message)
    else:
        homescr()
    main()

def datawarn():
    if os.path.exists('results'):
        print('This will wipe ALL DATA in the \'results\' folder, are you sure? (y/n)')
        sure = input('(choose y or n): ')
        if sure == 'y':
            sure = True
        else:
            sure = False
    else:
        sure = True
    return sure

def main():
    config = cfp.ConfigParser()
    config.read('config.ini')
    outpath = config['path']['output']
    action = input('  Enter the number of the action: ')
    if action == '1':
        warn = datawarn()
        if warn:
            if os.path.exists(f'{outpath}\\results\\beatmap') and os.path.exists(f'{outpath}\\results\\skin'):
                shutil.rmtree(f'{outpath}\\results')
                os.makedirs(f'{outpath}\\results\\beatmap')
                os.makedirs(f'{outpath}\\results\\skin')
                bmappack(f'{outpath}\\results\\beatmap')
                skinpack(f'{outpath}\\results\\skin')
            elif os.path.exists(f'{outpath}\\results\\beatmap'):
                shutil.rmtree(f'{outpath}\\results')
                os.makedirs(f'{outpath}\\results\\beatmap')
                os.makedirs(f'{outpath}\\results\\skin')
                bmappack(f'{outpath}\\results\\beatmap')
                skinpack(f'{outpath}\\results\\skin')
            elif os.path.exists(f'{outpath}\\results\\skin'):
                shutil.rmtree(f'{outpath}\\results')
                os.makedirs(f'{outpath}\\results\\beatmap')
                os.makedirs(f'{outpath}\\results\\skin')
                bmappack(f'{outpath}\\results\\beatmap')
                skinpack(f'{outpath}\\results\\skin')
            else:
                os.makedirs(f'{outpath}\\results\\beatmap')
                os.makedirs(f'{outpath}\\results\\skin')
                bmappack(f'{outpath}\\results\\beatmap')
                skinpack(f'{outpath}\\results\\skin')
            print('Packing complete!')
            packagain()
        else:
            print('Packing cancelled')
            menu()
    elif action == '2':
        warn = datawarn()
        if warn:
            if os.path.exists(f'{outpath}\\results\\beatmap'):
                shutil.rmtree(f'{outpath}\\results')
                os.makedirs(f'{outpath}\\results\\beatmap')
                bmappack(f'{outpath}\\results\\beatmap')
            else:
                os.makedirs(f'{outpath}\\results\\beatmap')
                bmappack(f'{outpath}\\results\\beatmap')
            print('Packing complete!')
            packagain()
        else:
            print('Packing cancelled')
            menu()
    elif action == '3':
        warn = datawarn()
        if warn:
            if os.path.exists(f'{outpath}\\results\\skin'):
                shutil.rmtree(f'{outpath}\\results')
                os.makedirs(f'{outpath}\\results\\skin')
                skinpack(f'{outpath}\\results\\skin')
            else:
                os.makedirs(f'{outpath}\\results\\skin')
                skinpack(f'{outpath}\\results\\skin')
            print('Packing complete!')
            packagain()
        else:
            print('Packing cancelled')
            menu()
    elif action == '4':
        config = cfp.ConfigParser()
        config.read('config.ini')
        print('Enter the new output path (default is the app folder, set it to blank to use the default):')
        outpath = input(f'(default is {cwd}): ')
        if outpath == '':
            outpath = cwd
        if os.path.exists(outpath):
            config['path']['output'] = outpath
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            menu('Output path changed!')
        else:
            menu('This path does not exist!')

    elif action == '5':
        print('Bye!')
        sys.exit()
    else:
        menu('Invalid action! Try again.')

if __name__ == '__main__':
    menu()