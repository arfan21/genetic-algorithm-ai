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
panjangPopulasi = 12

# buat suatu fungsi untuk membuat kromosom (random)


def createKromosom(panjangKromosom):
    kromosom = []
    for i in range(panjangKromosom):
        kromosom.append(random.randint(0, 1))
    return kromosom

# buat suatu fungsi untuk membuat populasi (kumpulan dari kromosom)


def generatePopulasi(panjangPopulasi):
    populasi = []
    for i in range(panjangPopulasi):
        populasi.append(createKromosom(panjangKromosom))
    return populasi

# fungsi genotif
# buat perulangan yang dapat menghitung genotif setiap populasi

# Didalam loop, masukkan rumus genotif
# genotif = batas bawah + ((batas atas - batas bawah) / 2**(-(i+1))) * (kromosom[i] * 2**(-(i+1))))


def genotifX(kromosom):
    pembagi = 0
    pengkali = 0
    for i in range(len(kromosom)):
        pembagi = pembagi + (2 ** (-(i+1)))
        pengkali = pengkali + kromosom[i]*2**(-(i+1))

    return batasBawahX + (((batasAtasX - batasBawahX) / pembagi) * pengkali)


def genotifY(kromosom):
    pembagi = 0
    pengkali = 0
    for i in range(len(kromosom)):
        pembagi = pembagi + (2 ** (-(i+1)))
        pengkali = pengkali + kromosom[i]*2**(-(i+1))

    return batasBawahY + (((batasAtasY - batasBawahY) / pembagi) * pengkali)

# buat fungsi fenotipe dengan memanggil fungsi genotif sebelumnya
# triknya panjang kromoson di bagi 2
# 0 1 0 | 0 1 0

# x1 = (panggil fungsi genotif())
# x2 = (panggil fungsi genotif())

# return x1,x2


def fenotip(populasi):
    x = []
    for i in range(len(populasi)):
        fullKromosom = np.array(populasi[i])
        kromosom1 = np.split(fullKromosom, 2)[0]
        kromosom2 = np.split(fullKromosom, 2)[1]
        x1 = genotifX(kromosom1)
        x2 = genotifY(kromosom2)
        x.append({i: {
            "x": x1,
            "y": x2,
        }})
    return x


# print fungsi fenotipe dengan memasukan kumpulan populasi yang telah kita buat


# buat fungsi rumus
def rumus(x, y):
    # masukkan rumus
    return np.cos(x**2) * np.sin(y**2) + (x+y)


# buat fungsi fitness untuk menghitung fitness setiap kromosom
# nilai x1 dan x2 di masukkan kedalam fungsi rumus
# fitness = -rumus(x1,x2)
# return fitness
def fitness(x1, x2):
    return -1 * rumus(x1, x2)

# buat fungsi evaluate yang mereturn nilai kumpulan fitness setiap populasi


def evaluate(allFenotip):
    allResult = []
    for i in range(len(allFenotip)):
        fenotip = allFenotip[i]

        x1 = fenotip[i]["x"]
        x2 = fenotip[i]["y"]
        fenotip[i]["fitness"] = fitness(x1, x2)
        allResult.append(fenotip)
    return allResult


def getFitnessValue(x):
    [[key, value]] = x.items()

    return x[key]["fitness"]

# buat fungsi elitism
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
# urutkan populasi berdasarkan nilai fitness nya
# print 1 populasi yang paling baik (tinggi nilai fitnessnya)


def parentSelection(allResultEvaluate):
    # Menggunakan tournament selection
    best = {}

    for i in range(len(allResultEvaluate)):
        indv = allResultEvaluate[random.randint(0, len(allResultEvaluate) - 1)]
        [[keyIndv, itemIndv]] = indv.items()

        # if best == [] or fitness(indv) > fitness(best)
        if len(best) == 0:
            best = indv
        else:
            [[keyBest, itemBest]] = best.items()
            if itemIndv["fitness"] > itemBest["fitness"]:
                best = indv

    return keyBest


# buat fungsi crossover
def crossover(kromosom1, kromosom2):
    offspring1 = []
    offspring2 = []
    chance = random.randint(0, 70)
    # if temp <= 0.7
    if chance <= 70:
        # buat titik potong, misalnya offspring = p1[:titik_potong] + p2[titik_potong:]
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
    # return offspring
    return offspring1, offspring2

    # p1 = parentSelection(Populasi, Kromosom)) [0,1] [0,1]
    # p2 = parentSelection(Populasi, Kromosom)) [1,1] [0,1]
    # crossover(p1,p2)

    # offspring_p1 = [0,1] + [0,1]

    # offspring_p2 =

    # buat fungsi mutasi


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
    # Pm =  0.1

    # hasilRandom = random.random()
    # if hasilRand < 0.1 :
    # random terus menerus
    # return hasil random

    # panggil fungsi mutasi, parameternya setiap kromosom

    # buat fungsi main atau code untuk memanggil semua fungsi2 yang telah dibuat


def main():
    # populasi = generatePopulasi(panjangPopulasi)
    # print("Populasi :", populasi)
    # allFenotip = fenotip(populasi, batasBawahX, batasAtasX)
    # print("fenotip : ", allFenotip)
    # allFitness = evaluate(allFenotip)
    # elitism(populasi, allFitness)
    # parent1 = parentSelection(allFitness)
    # parent2 = parentSelection(allFitness)
    # print(f"parent 1 : {parent1}, parent 2 : {parent2}")
    # offspring1, offspring2 = crossover(populasi[parent1], populasi[parent2])
    # print(offspring1, offspring2)
    # print(mutasi(offspring1), mutasi(offspring2))
    populasi = generatePopulasi(panjangPopulasi)

    for gen in range(1, 20):
        allFenotip = fenotip(populasi)
        allFitness = evaluate(allFenotip)
        newPopulation = elitism(populasi, allFitness)
        while(len(newPopulation) < panjangPopulasi):
            parent1 = parentSelection(allFitness)
            parent2 = parentSelection(allFitness)
            offspring1, offspring2 = crossover(
                populasi[parent1], populasi[parent2])
            offspring1 = mutasi(offspring1)
            offspring2 = mutasi(offspring2)
            newPopulation.append(offspring1)
            newPopulation.append(offspring2)
        populasi = newPopulation

    allFenotip = fenotip(populasi)
    allFitness = evaluate(allFenotip)
    bestIndex = parentSelection(allFitness)
    sortedFitness = sorted(
        allFitness, key=getFitnessValue, reverse=True)
    for fit in sortedFitness:
        print(f"All Fitness: {fit}")

    print(f"Best Kromosom : {populasi[bestIndex]}")
    print(f"Best Fitness : {sortedFitness[0]}")


if __name__ == "__main__":
    main()
# return populasi terbaik dan nilai fenotypenya
