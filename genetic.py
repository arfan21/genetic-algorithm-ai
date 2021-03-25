import random
import numpy as np

# batas1

batasAtasX = 2
batasBawahX = -1

# batas2

batasAtasY = 1
batasBawahY = -1

# panjang kromosom

panjangKromosom = 18

# panjang populasi

panjangPopulasi = 16

# panjang gen

panjangGen = 50

# fungsi untuk membuat kromosom (random)


def createKromosom(panjangKromosom):
    kromosom = []
    for i in range(panjangKromosom):
        kromosom.append(random.randint(0, 1))
    return kromosom

# fungsi untuk membuat populasi (kumpulan dari kromosom)


def generatePopulasi(panjangPopulasi):
    populasi = []
    for i in range(panjangPopulasi):
        populasi.append(createKromosom(panjangKromosom))
    return populasi

# fungsi genotif
# perulangan yang dapat menghitung menghitung pembagi dan pengkali


def genotif(kromosom, batasBawah, batasAtas):
    pembagi = 0
    pengkali = 0
    for i in range(len(kromosom)):
        pembagi = pembagi + (2 ** (-(i+1)))
        pengkali = pengkali + kromosom[i]*2**(-(i+1))

    return batasBawah + (((batasAtas - batasBawah) / pembagi) * pengkali)


# fungsi fenotipe dengan memanggil fungsi genotif sebelumnya
# panjang kromoson di bagi 2
# 0 1 0 | 0 1 0
# x1 = (panggil fungsi genotif())
# x2 = (panggil fungsi genotif())

# return x,y


def fenotip(populasi):
    xy = []
    for i in range(len(populasi)):
        fullKromosom = np.array(populasi[i])
        splitedKromosom = np.split(fullKromosom, 2)
        kromosom1 = splitedKromosom[0]
        kromosom2 = splitedKromosom[1]

        x = genotif(kromosom1, batasBawahX, batasAtasX)
        y = genotif(kromosom2, batasBawahY, batasAtasY)
        xy.append({i: {
            "x": x,
            "y": y,
        }})
    return xy


# fungsi rumus
def rumus(x, y):
    # masukkan rumus
    return ((np.cos(x**2)) * (np.sin(y**2))) + (x+y)


# fungsi fitness untuk menghitung fitness setiap kromosom
# nilai x1 dan x2 di masukkan kedalam fungsi rumus
# fitness = -rumus(x1,x2)
# return fitness
def fitness(x, y):
    return rumus(x, y)

# fungsi evaluate yang mereturn nilai kumpulan fitness setiap populasi


def evaluate(allFenotip):
    allResult = []
    for i in range(len(allFenotip)):
        fenotip = allFenotip[i]

        x = fenotip[i]["x"]
        y = fenotip[i]["y"]
        fenotip[i]["fitness"] = fitness(x, y)
        allResult.append(fenotip)
    return allResult


def getFitnessValue(x):
    [[key, value]] = x.items()

    return x[key]["fitness"]

# fungsi elitism
# urutkan populasi berdasarkan nilai fitness tertinggi
# bagi dua jumlah populasi
# print populasi terbaik (setelah dibagi 2)


def elitism(populasi, allFitness):
    sortedFitness = sorted(
        allFitness, key=getFitnessValue, reverse=True)

    resultAsNParray = np.array(sortedFitness)

    resultKebagi = np.split(resultAsNParray, 2)

    newPopulasi = []
    for index in range(len(resultKebagi[0])):
        item = resultKebagi[0][index]
        [[key, value]] = item.items()

        newPopulasi.append(populasi[key])
    return newPopulasi

# buat fungsi parent selection
# buat variable yang dapat menampung kromosom populasi secara random (dibagi 2) = 14
# masukan ke fungsi evaluate = menghasilkan nilai fitness
# mengurutkan populasi berdasarkan nilai fitness nya
# return index populasi terbaik


def parentSelection(allResultEvaluate):
    # Menggunakan tournament selection
    best = {}

    for i in range(len(allResultEvaluate)):
        indv = allResultEvaluate[random.randint(0, len(allResultEvaluate) - 1)]
        [[keyIndv, itemIndv]] = indv.items()

        if len(best) == 0:
            best = indv
        else:
            [[keyBest, itemBest]] = best.items()

            if itemIndv["fitness"] > itemBest["fitness"]:
                best = indv
    [[keyBest, itemBest]] = best.items()
    return keyBest

# fungsi crossover
# return offspring


def crossover(kromosom1, kromosom2):
    offspring1 = []
    offspring2 = []
    chance = random.randint(0, 70)
    if chance <= 70:
        # titik potong, misalnya offspring = p1[:titik_potong] + p2[titik_potong:]
        for i in range(panjangKromosom):
            if i < ((panjangKromosom // 2)-1):
                offspring1.append(kromosom1[i])
                offspring2.append(kromosom2[i])
            else:
                offspring1.append(kromosom2[i])
                offspring2.append(kromosom1[i])
    else:
        offspring1 = kromosom1
        offspring2 = kromosom2
    return offspring1, offspring2

# fungsi mutasi
# Pm =  0.1
# hasilRandom = random.random()
# if hasilRand < 0.1 :
# random terus menerus
# return hasil random


def mutasi(offspring):
    mutant = []
    chance = random.randint(0, 10)
    if chance <= 10:
        mutant = offspring
        iRand = random.randint(0, len(offspring))
        for i in range(len(mutant)):
            if i == iRand:
                mutant[i] = random.randint(0, 1)
    else:
        mutant = offspring
    return mutant


def seleksiSurvivorForNextGen(populasi, newPopulasi, allFitness):
    while(len(newPopulasi) < panjangPopulasi):
        parent1 = parentSelection(allFitness)
        parent2 = parentSelection(allFitness)
        offspring1, offspring2 = crossover(
            populasi[parent1], populasi[parent2])
        offspring1 = mutasi(offspring1)
        offspring2 = mutasi(offspring2)
        newPopulasi.append(offspring1)
        newPopulasi.append(offspring2)

        if len(newPopulasi) > panjangPopulasi:
            newPopulasi.pop()
    return newPopulasi

# fungsi main atau code untuk memanggil semua fungsi2 yang telah dibuat
# return populasi terbaik dan nilai fenotypenya


def main():
    populasi = generatePopulasi(panjangPopulasi)

    # mencari populasi terbaik sampai generasi ke 20
    for gen in range(1, panjangGen + 1):
        allFenotip = fenotip(populasi)
        allFitness = evaluate(allFenotip)
        newPopulasi = elitism(populasi, allFitness)
        if gen == 1:
            sortedFitness = sorted(
                allFitness, key=getFitnessValue, reverse=True)
            [[firstGenBestIndex, Fitness]] = sortedFitness[0].items()
            print(
                f"First Kromosom : {populasi[firstGenBestIndex]}")
            print(f"First Fitness : {sortedFitness[0]}")

        populasi = seleksiSurvivorForNextGen(populasi, newPopulasi, allFitness)
    print(f"\n--------------- Setelah {panjangGen} Generasi ---------------\n")
    allFenotip = fenotip(populasi)
    allFitness = evaluate(allFenotip)
    sortedFitness = sorted(
        allFitness, key=getFitnessValue, reverse=True)
    [[bestIndex, Fitness]] = sortedFitness[0].items()
    print(f"Best Kromosom : {populasi[bestIndex]}")
    print(f"Best Fitness : {Fitness}")


if __name__ == "__main__":
    main()
