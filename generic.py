import random
import numpy as np
# batas1
batasAtasX = 2
batasBawahX = -1
# batas2
batasAtasY = 1
batasBawahY = -1
# input jumlah kromosom
panjangKromosom = 14
# input jumlah populasi
panjangPopulasi = 10

# buat suatu fungsi untuk membuat kromosom (random)


def createKromosom(panjangKromosom):
    kromosom = []
    for i in range(panjangKromosom):
        kromosom.append(random.randint(0, 1))
    return kromosom
# Kromosom : [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0]
# buat suatu fungsi untuk membuat populasi (kumpulan dari kromosom)


def generatePopulasi(panjangPopulasi):
    populasi = []
    for i in range(panjangPopulasi):
        populasi.append(createKromosom(10))
    return populasi

# Populasi : [[1, 0, 0, 1, 0, 1, 1, 1, 1, 1], [0, 0, 1, 0, 1, 1, 1, 0, 1, 1], [0, 0, 1, 1, 0, 1, 1, 0, 1, 1], [1, 0, 0, 0, 0, 0, 0, 1, 1, 1], [1, 0, 1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 1, 1], [0, 1, 1, 0, 0, 0, 1, 0, 1, 0], [1, 0, 0, 1, 1, 1, 0, 0, 1, 0], [1, 1, 1, 1, 0, 0, 1, 0, 0, 1]]

# fungsi genotif
# buat perulangan yang dapat menghitung genotif setiap populasi

# Didalam loop, masukkan rumus genotif
# genotif = batas bawah + ((batas atas - batas bawah) / 2**(-(i+1))) * (kromosom[i] * 2**(-(i+1))))


def genotif(kromosom, batasBawah, batasAtas):
    pembagi = 0
    pengkali = 0
    for i in range(len(kromosom)):
        pembagi = pembagi + (2 ** (-(i+1)))
        pengkali = pengkali + kromosom[i]*2**(-(i+1))

    return batasBawah + (((batasAtas - batasBawah) / pembagi) * pengkali)


populasi = generatePopulasi(panjangPopulasi)
print("Populasi :", populasi)


# buat fungsi fenotipe dengan memanggil fungsi genotif sebelumnya
# triknya panjang kromoson di bagi 2
# 0 1 0 | 0 1 0

# x1 = (panggil fungsi genotif())
# x2 = (panggil fungsi genotif())

# return x1,x2

def fenotip(populasi, batasBawah, batasAtas):
    x = []
    for i in range(len(populasi)):
        fullKromosom = np.array(populasi[i])
        kromosom1 = np.split(fullKromosom, 2)[0]
        kromosom2 = np.split(fullKromosom, 2)[1]
        x1 = genotif(kromosom1, batasBawah, batasAtas)
        x2 = genotif(kromosom2, batasBawah, batasAtas)
        x.append({i: {
            "x1": x1,
            "x2": x2,
        }})
    return x


# print fungsi fenotipe dengan memasukan kumpulan populasi yang telah kita buat
allFenotip = fenotip(populasi, batasBawahX, batasAtasX)
print("fenotip : ", allFenotip)


# buat fungsi rumus
def rumus(x, y):
    # masukkan rumus
    return np.cos(x*x) * np.sin(y*y) + (x+y)


# buat fungsi fitness untuk menghitung fitness setiap kromosom
# nilai x1 dan x2 di masukkan kedalam fungsi rumus
#fitness = -rumus(x1,x2)
# return fitness
def fitness(x1, x2):
    return -1 * rumus(x1, x2)

# buat fungsi evaluate yang mereturn nilai kumpulan fitness setiap populasi


def evaluate(allFenotip):
    allResult = []
    for i in range(len(allFenotip)):
        fenotip = allFenotip[i]

        x1 = fenotip[i]["x1"]
        x2 = fenotip[i]["x2"]
        fenotip[i]["fitness"] = fitness(x1, x2)
        allResult.append(fenotip)
    return allResult

    # return allResult

# buat fungsi elitism
# urutkan populasi berdasarkan nilai fitness tertinggi
# bagi dua jumlah populasi
# print populasi terbaik (setelah dibagi 2)


# {1: {'x1': 1.6129032258064515, 'x2': 1.8064516129032255, 'fitness': -3.523450555718238}}


def getFitnessValue(x):
    thisISkey = 0
    [[key, value]] = x.items()

    return x[key]["fitness"]


def elitism(populasi, allFenotip):
    allResult = evaluate(allFenotip)
    sortedResult = sorted(
        allResult, key=getFitnessValue, reverse=True)

    resultAsNParray = np.array(sortedResult)
    resultKebagi = np.split(resultAsNParray, 2)

    newPopulasi = []
    for index in range(len(resultKebagi[0])):
        item = resultKebagi[0][index]
        [[key, value]] = item.items()

        newPopulasi.append(populasi[key])
    print("selected popoulasi: ", newPopulasi)


elitism(populasi, allFenotip)

# buat fungsi parent selection
# buat variable yang dapat menampung kromosom populasi secara random (dibagi 2) = 14
# masukan ke fungsi evaluate = menghasilkan nilai fitness
# urutkan populasi berdasarkan nilai fitness nya
# print 1 populasi yang paling baik (tinggi nilai fitnessnya)

# buat fungsi crossover
# if temp <= 0.7
# buat titik potong, misalnya offspring = p1[:titik_potong] + p2[titik_potong:]
# return offspring

# p1 = parentSelection(Populasi, Kromosom)) [0,1] [0,1]
# p2 = parentSelection(Populasi, Kromosom)) [1,1] [0,1]
# crossover(p1,p2)

# offspring_p1 = [0,1] + [0,1]

# offspring_p2 =

# buat fungsi mutasi
#Pm =  0.1

#hasilRandom = random.random()
# if hasilRand < 0.1 :
# random terus menerus
# return hasil random

# panggil fungsi mutasi, parameternya setiap kromosom

# buat fungsi main atau code untuk memanggil semua fungsi2 yang telah dibuat
# if __name__ == "__main__":
# return populasi terbaik dan nilai fenotypenya
