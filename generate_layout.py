import random
import copy
from operator import attrgetter

from deap import base
from deap import creator
from deap import tools

from layout import Layout

toolbox = base.Toolbox()
toolbox.register("population", tools.initRepeat, list, Layout)


def main():
    #random.seed(64)

    pop = toolbox.population(n=300)

    CXPB, MUTPB = 0.5, 0.8

    print("Start of evolution")

    for ind in pop:
        ind.evaluate()

    print("  Evaluated %i individuals" % len(pop))

    g = 0
    best_ind = None
    best_one_remaining = 0
    while g < 600:
        g = g + 1
        print("-- Generation %i --" % g)

        offspring = Layout.tournament(pop, len(pop), 3)
        offspring = list(map(toolbox.clone, offspring))

        children = []
        for p1, p2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                children.append(Layout(p1, p2))
                children.append(Layout(p1, p2))
            else:
                children.append(p1)
                children.append(p2)

        offspring = children

        redundancies = []
        for o in offspring:
            if o.layout in redundancies:
                if random.random() < 0.6:
                    o.mutate()
                elif random.random() < 0.7:
                    o.mutate(indpb=0.2)
                elif random.random() < 0.8:
                    o.mutate(indpb=0.4)
                elif random.random() < 0.9:
                    o.mutate(indpb=0.7)
                else:
                    o.mutate(indpb=0.9)
            else:
                redundancies.append(o.layout)

        for ind in offspring:
            if ind.fitness == 0:
                ind.evaluate()

        random.shuffle(offspring)

        pop[:] = offspring

        tmp = min(pop, key=attrgetter('fitness'))
        if not best_ind:
            best_ind = tmp
            print(best_ind)
            print(best_ind.fitness)
        elif tmp.fitness < best_ind.fitness:
            best_ind = tmp
            best_one_remaining = 0
            print(best_ind)
            print(best_ind.fitness)
        else:
            best_one_remaining += 1
            print('wasn\'t updated %i times' % best_one_remaining)
            print(tmp.fitness)
        print()

    print("-- End of (successful) evolution --")

    print(best_ind)
    print(best_ind.fitness)

if __name__ == "__main__":
    main()

