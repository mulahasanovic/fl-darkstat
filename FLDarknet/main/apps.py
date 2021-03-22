from django.apps import AppConfig
from django.conf import settings
import re

data = {}
infocards = {}

def strip_from_rn(a):
    return a.replace("\r","").replace("\n","")

def parse_infocards(filename):
    import codecs
    f = codecs.open( filename, "r", "utf-8" )
    #f = open(filename)

    content = f.readlines()
    
    regex_numbers = "^\d+\r|^\d+\n"
    output = {}
    line_count = len(content)
    #breakpoint()
    for i in range(line_count):
        #print(content[i])
        if (re.search(regex_numbers, content[i]) is not None):
            try:
                output[int(strip_from_rn(content[i]))] = [strip_from_rn(content[i+1]), strip_from_rn(content[i+2])]
            except:
                print('ERR in infocards parser')
        
    i+=1
    return output

def parse_file(filename):
    #breakpoint()
    f = open(filename)
    content = f.readlines()
    
    output = {}
    regex_for_headers = "(\[)\w+(\])"

    line_count = len(content)
    for i in range(line_count):
        if (re.search(regex_for_headers, content[i]) is not None):
            header = content[i].lower().replace("\n","")

            if header not in output.keys():
                output[header] = []

            i+=1
            obj = {}
            while (
                (re.search(regex_for_headers, content[i+1]) is None) and 
                (i < (line_count - 2))
                ):

                if (content[i] == '\n'):
                    i+=1
                    continue
                
                if (re.search("^(;)", content[i]) is not None):
                    i+=1
                    continue

                splitted = content[i].replace(" ","").replace("\n","").split('=')

                if len(splitted) == 2:
                    if splitted[0] not in obj.keys():
                        obj[splitted[0]] = []

                    if ',' not in splitted[1]:
                        obj[splitted[0]].append(splitted[1])
                    else:
                        obj[splitted[0]].append(splitted[1].split(','))
                else:
                    print('ERR splitted')
                i += 1

            output[header].append(obj)

        i+=1
    return output

def view_wrapper(obj, cl, name):
    if name in obj.keys():
        obj[name] = cl(obj[name][0])

def view_wrapper_with_infocard(obj, cl, name, infoname):
    if name in obj.keys():
        obj[name] = cl(obj[name][0])
        if obj[name] in infocards:
            obj[infoname] = (infocards[obj[name]][1])

def fill_commodity_table(Commodity):
    #COMMODITY TABLE
    Commodity.objects.all().delete()

    goods = data['select_equip.ini']
    arr = goods['[commodity]'].copy()
    for obj in arr:
        try:
            view_wrapper_with_infocard(obj, int, 'ids_name', 'name')
            view_wrapper_with_infocard(obj, int, 'ids_info', 'infocard')
            view_wrapper(obj, int, 'units_per_container')
            view_wrapper(obj, int, 'decay_per_second')
            view_wrapper(obj, int, 'hit_pts')
            view_wrapper(obj, str, 'pod_appearance')
            view_wrapper(obj, str, 'loot_appearance')
            view_wrapper(obj, str, 'nickname')
            view_wrapper(obj, float, 'volume')

            c = Commodity(
                **obj
            )
            c.save()
        except:
            print("ERR in filling commodities", obj)

class MainConfig(AppConfig):
    name = 'main'
    def ready(self):
        #import flint
        #flint.paths.set_install_path('Freelancer')
        #comms= flint.get_commodities()
        from commodities.models import Commodity

        global data
        #breakpoint()
        from os import walk
        import os
        for (dirpath, dirnames, filenames) in walk(settings.EQUIPMENT_DIR):
            for filename in filenames:
                try:
                    data[filename] = parse_file(os.path.join(settings.EQUIPMENT_DIR,filename))
                except:
                    print('ERROR in ', filename)
            break

        global infocards
        infocards = parse_infocards(settings.INFOCARDS_PATH)

        fill_commodity_table(Commodity)

        # for filename in data.keys():
        #     for header in data[filename].keys():
        #         for obj in data[filename][header]:
        #             #print(obj)
        #             #breakpoint()
        #             break
            
        
        # goods = parse_file(settings.GOODS_DIR)
        # select_equip = parse_file(settings.SEL_EQUIP_DIR)
        # market_commodities = parse_file(settings.MARKET_DIR)

# test = set()
# goods = data['select_equip.ini']
# arr = goods['[commodity]']
# for obj in arr:
#     for key in obj.keys():
#         if key not in test:
#             print(key, " = ", obj[key])
#             test.add(key)

# goods = data['select_equip.ini']
# arr = goods['[commodity]']
# for obj in arr:
#     if 'ids_name' in obj.keys():
#         ids = int(obj['ids_name'][0])
#         if ids in infocards:
#             print(infocards[ids])
#         else:
#             break
#             breakpoint()
#             print('ERR in test 1')

# possible_keys = set()
# for key in goods.keys():
#     #if 'category' in goods[key].keys() and goods[key]['category'] == 'equipment':
#     for subkey in goods[key].keys():   
#         if 'category' in subkey:
#             possible_keys.add(goods[key][subkey]) 
# print(possible_keys)

# for key in goods.keys():
#     if 'commodity' in key:
#         print(goods[key])

# for key in goods.keys():
#     for subkey in goods[key].keys():
#         if isinstance(goods[key][subkey], list):
#             if ('addon' not in subkey):
#                 print('ERR not addon')

                    

        # for i in range(10):
        #     c = Commodity(
        #         name = str(i)
        #     )
        #     c.save()

            # for obj in comms:
            #     c = Commodity(
            #         name = obj.name(),
            #         nickname = obj.nickname,
            #         ids_name = obj.ids_name,
            #         ids_info = obj.ids_info,
            #         lootable = obj.lootable,
            #         decay_per_second = obj.decay_per_second,
            #         volume = obj.volume,
            #     )
            #     c.save()