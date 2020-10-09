#!/usr/bin/env python3

"""
Given an initial set of coordinates, to be used with the fill command in
Minecraft, perform the math necessary to expand, contract, and raise/lower the
area determined by the coordinates. The number of blocks high may also be set
when prompted for a range for height. Note: when setting a range for height,
treat the first group of coordinates as the lower Y value.
The final adjusted result may replace the values of the coordinates to be
processed, allowing adjustments to the new values.

Fill command syntax:
/fill -75 92 -864 -117 92 -900 air

Last Update: 2020-10-08 07:49 CDT
"""

# Assign variables to be used for indexing in coordinate lists
X, Y, Z = 0, 1, 2


def set_coord() -> tuple[list[int], list[int]]:
    """
    Prompt user for two sets of coordinates, convert input to lists of ints.
    Valid input consists of whole numbers separated by commas; spaces are
    removed.
    """
    while True:
        fg_text = input("Starting coordinates (X,Y,Z): ").replace(" ", "")
        sg_text = input("Ending coordinates (X,Y,Z): ").replace(" ", "")
        try:
            first_group = [int(item) for item in fg_text.split(",")]
            second_group = [int(item) for item in sg_text.split(",")]
        except ValueError:
            print("\nError: you must enter whole numbers separated by commas.")
        else:
            if len(first_group) == 3 == len(second_group):
                return first_group, second_group
            else:
                print("\nError: coordinates must have three values each.")


def adj_coord(f_group: list[int],
              s_group: list[int],
              expand: bool = True) -> tuple[list[int], list[int]]:
    """
    Given two lists of coordinates, compare values and perform necessary
    operations to expand or contract the area determined by the coordinates.
    Build and return lists holding resulting coordinate values.

    :param f_group: first list of coordinates.
    :param s_group: second list of coordinates.
    :param expand: expand if True, otherwise contract; default is expand.
    :return: new lists with adjusted coordinates.
    """
    while True:
        try:
            adjust_by = int(input("Blocks to adjust by: "))
        except ValueError:
            print("\nError: you must enter a whole number.")
        else:
            adj = adjust_by if expand else -adjust_by
            break

    new_f_group = []
    new_s_group = []

    # process X coordinates
    if f_group[X] > s_group[X]:
        new_f_group.append(f_group[X] + adj)
        new_s_group.append(s_group[X] - adj)
    elif f_group[X] < s_group[X]:
        new_f_group.append(f_group[X] - adj)
        new_s_group.append(s_group[X] + adj)
    else:  # the X coordinates are the same
        new_f_group.append(f_group[X])
        new_s_group.append(s_group[X])

    # adj_coord does not process height (Y); always keeps the original values
    new_f_group.append(f_group[Y])
    new_s_group.append(s_group[Y])

    # process Z coordinates
    if f_group[Z] > s_group[Z]:
        new_f_group.append(f_group[Z] + adj)
        new_s_group.append(s_group[Z] - adj)
    elif f_group[Z] < s_group[Z]:
        new_f_group.append(f_group[Z] - adj)
        new_s_group.append(s_group[Z] + adj)
    else:  # the Z coordinates are the same
        new_f_group.append(f_group[Z])
        new_s_group.append(s_group[Z])

    return new_f_group, new_s_group


def main():
    """ Loop to provide menu for user interaction. """
    fg, sg = set_coord()  # initial values (fg: first group, sg: second group)

    while True:
        # display coordinates to be processed in loop body
        print("\nCoordinates:", *fg, *sg)

        option = input("Expand(e), Contract(c), Neither(n), Reset(r), "
                       "Quit(q): ").strip().lower()

        if option == 'e':
            nfg, nsg = adj_coord(fg, sg)
        elif option == 'c':
            nfg, nsg = adj_coord(fg, sg, False)
        elif option == 'n':
            # no changes to X and Z coordinates; copy original values
            nfg, nsg = list(fg), list(sg)
        elif option == 'r':
            fg, sg = set_coord()
            continue
        elif option == 'q':
            print("\nGoodbye.")
            break
        else:
            print(f'\nError: option "{option}" is not a valid selection.')
            continue

        try:
            height_adj = int(input("Adjust height by: "))
        except ValueError:
            print("\nError: "
                  "invalid entry. Height adjustment has been set to 0.")
            height_adj = 0

        # apply height adjustment value to y coordinates
        nfg[Y] += height_adj
        nsg[Y] += height_adj

        # prompt for height range and apply if present
        set_range = input("Specify range for height? (y/n): ").strip().lower()
        if set_range in ('y', 'yes'):
            while True:
                print(f"\nBlocks begin at a height of {nfg[Y]}")
                try:
                    range_amt = int(input("Blocks high: ")) - 1
                except ValueError:
                    print("\nError: "
                          "you must enter a whole number of 1 or more.")
                    continue
                if range_amt < 0:
                    print("\nError: you must enter 1 or more blocks.")
                else:
                    nsg[Y] = nfg[Y] + range_amt
                    break

        # display results of calculations
        print("\nResults:", *nfg, *nsg)

        while True:
            replace = input("Replace active coordinates? "
                            "(y/n): ").strip().lower()
            if replace in ('y', 'yes'):
                fg, sg = nfg, nsg
                print("Coordinates replaced.")
                break
            elif replace in ('n', 'no'):
                break
            else:
                print(f'\nError: "{replace}" is not a valid selection.')


if __name__ == '__main__':
    main()
