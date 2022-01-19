from typing import Iterable, Union, SupportsInt, Iterator, Callable, List, Tuple, Dict, Optional
import copy
import dataclasses
import enum

Color = bool
COLORS = [BLACK, RED] = [False, True]
COLOR_NAMES = ["black", "red"]

PieceType = int
PIECE_TYPES = [PAWN, ROOK, KNIGHT, BISHOP, ADVISOR, KING, CANNON] = range(1, 8)
PIECE_SYMBOLS = [None, "p", "r", "n", "b", "a", "k", "c"]
PIECE_NAMES = [None, "pawn", "rook", "knight", "bishop", "advisor", "king", "cannon"]

UNICODE_PIECE_SYMBOLS = {
    "R": "俥", "r": "車",
    "N": "傌", "n": "馬",
    "B": "相", "b": "象",
    "A": "仕", "a": "士",
    "K": "帥", "k": "將",
    "P": "兵", "p": "卒",
    "C": "炮", "c": "砲"
}


def piece_symbol(piece_type: PieceType) -> str:
    return PIECE_SYMBOLS[piece_type]


def piece_name(piece_type: PieceType) -> str:
    return PIECE_NAMES[piece_type]


STARTING_FEN = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR r - - 0 1'
STARTING_BOARD_FEN = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR"


class Status(enum.IntFlag):
    VALID = 0
    EMPTY = 1 << 0
    TOO_MANY_RED_PIECES = 1 << 1
    TOO_MANY_BLACK_PIECES = 1 << 2
    NO_RED_KING = 1 << 3
    NO_BLACK_KING = 1 << 4
    TOO_MANY_RED_KINGS = 1 << 5
    TOO_MANY_BLACK_KINGS = 1 << 6
    RED_KING_PLACE_WRONG = 1 << 7
    BLACK_KING_PLACE_WRONG = 1 << 8
    TOO_MANY_RED_PAWNS = 1 << 9
    TOO_MANY_BLACK_PAWNS = 1 << 10
    RED_PAWNS_PLACE_WRONG = 1 << 11
    BLACK_PAWNS_PLACE_WRONG = 1 << 12
    TOO_MANY_RED_ROOKS = 1 << 13
    TOO_MANY_BLACK_ROOKS = 1 << 14
    TOO_MANY_RED_KNIGHTS = 1 << 15
    TOO_MANY_BLACK_KNIGHTS = 1 << 16
    TOO_MANY_RED_BISHOPS = 1 << 17
    TOO_MANY_BLACK_BISHOPS = 1 << 18
    RED_BISHOPS_PLACE_WRONG = 1 << 19
    BLACK_BISHOPS_PLACE_WRONG = 1 << 20
    TOO_MANY_RED_ADVISORS = 1 << 21
    TOO_MANY_BLACK_ADVISORS = 1 << 22
    RED_ADVISORS_PLACE_WRONG = 1 << 23
    BLACK_ADVISORS_PLACE_WRONG = 1 << 24
    TOO_MANY_RED_CANNONS = 1 << 25
    TOO_MANY_BLACK_CANNONS = 1 << 26
    OPPOSITE_CHECK = 1 << 27


STATUS_VALID = Status.VALID
STATUS_EMPTY = Status.EMPTY
STATUS_TOO_MANY_RED_PIECES = Status.TOO_MANY_RED_PIECES
STATUS_TOO_MANY_BLACK_PIECES = Status.TOO_MANY_BLACK_PIECES
STATUS_NO_RED_KING = Status.NO_RED_KING
STATUS_NO_BLACK_KING = Status.NO_BLACK_KING
STATUS_TOO_MANY_RED_KINGS = Status.TOO_MANY_RED_KINGS
STATUS_TOO_MANY_BLACK_KINGS = Status.TOO_MANY_BLACK_KINGS
STATUS_RED_KING_PLACE_WRONG = Status.RED_KING_PLACE_WRONG
STATUS_BLACK_KING_PLACE_WRONG = Status.BLACK_KING_PLACE_WRONG
STATUS_TOO_MANY_RED_PAWNS = Status.TOO_MANY_RED_PAWNS
STATUS_TOO_MANY_BLACK_PAWNS = Status.TOO_MANY_BLACK_PAWNS
STATUS_RED_PAWNS_PLACE_WRONG = Status.RED_PAWNS_PLACE_WRONG
STATUS_BLACK_PAWNS_PLACE_WRONG = Status.BLACK_PAWNS_PLACE_WRONG
STATUS_TOO_MANY_RED_ROOKS = Status.TOO_MANY_RED_ROOKS
STATUS_TOO_MANY_BLACK_ROOKS = Status.TOO_MANY_BLACK_ROOKS
STATUS_TOO_MANY_RED_KNIGHTS = Status.TOO_MANY_RED_KNIGHTS
STATUS_TOO_MANY_BLACK_KNIGHTS = Status.TOO_MANY_BLACK_KNIGHTS
STATUS_TOO_MANY_RED_BISHOPS = Status.TOO_MANY_RED_BISHOPS
STATUS_TOO_MANY_BLACK_BISHOPS = Status.TOO_MANY_BLACK_BISHOPS
STATUS_RED_BISHOPS_PLACE_WRONG = Status.RED_BISHOPS_PLACE_WRONG
STATUS_BLACK_BISHOPS_PLACE_WRONG = Status.BLACK_BISHOPS_PLACE_WRONG
STATUS_TOO_MANY_RED_ADVISORS = Status.TOO_MANY_RED_ADVISORS
STATUS_TOO_MANY_BLACK_ADVISORS = Status.TOO_MANY_BLACK_ADVISORS
STATUS_RED_ADVISORS_PLACE_WRONG = Status.RED_ADVISORS_PLACE_WRONG
STATUS_BLACK_ADVISORS_PLACE_WRONG = Status.BLACK_ADVISORS_PLACE_WRONG
STATUS_TOO_MANY_RED_CANNONS = Status.TOO_MANY_RED_CANNONS
STATUS_TOO_MANY_BLACK_CANNONS = Status.TOO_MANY_BLACK_CANNONS
STATUS_OPPOSITE_CHECK = Status.OPPOSITE_CHECK

Square = int

COLUMN_NAMES = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
ROW_NAMES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


SQUARES = [
    A0, B0, C0, D0, E0, F0, G0, H0, I0,
    A1, B1, C1, D1, E1, F1, G1, H1, I1,
    A2, B2, C2, D2, E2, F2, G2, H2, I2,
    A3, B3, C3, D3, E3, F3, G3, H3, I3,
    A4, B4, C4, D4, E4, F4, G4, H4, I4,
    A5, B5, C5, D5, E5, F5, G5, H5, I5,
    A6, B6, C6, D6, E6, F6, G6, H6, I6,
    A7, B7, C7, D7, E7, F7, G7, H7, I7,
    A8, B8, C8, D8, E8, F8, G8, H8, I8,
    A9, B9, C9, D9, E9, F9, G9, H9, I9
] = range(90)

SQUARE_NAMES = [c + r for r in ROW_NAMES for c in COLUMN_NAMES]


def parse_square(name: str):
    """
    Gets the square index for the given square *name*
    (e.g., ``a1`` returns ``0``).

    :raises: :exc:`ValueError` if the square name is invalid.
    """
    return SQUARE_NAMES.index(name)


def square_name(square: Square):
    """Gets the name of the square, like ``a3``."""
    return SQUARE_NAMES[square]


def square(column_index: int, row_index: int):
    """Gets a square number by column and row index."""
    return row_index * 9 + column_index


def square_column(square: Square) -> int:
    """Gets the column index of the square where ``0`` is the a-column."""
    return square % 9


def square_row(square: Square) -> int:
    """Gets the row index of the square where ``0`` is the first row."""
    return square // 9


def square_distance(a: Square, b: Square) -> int:
    """
    Gets the distance (i.e., the number of king steps) from square *a* to *b*.
    """
    return max(abs(square_column(a) - square_column(b)), abs(square_row(a) - square_row(b)))


def square_mirror(square: Square) -> Square:
    """Mirrors the square vertically."""
    return 81 - square + ((square % 9) << 1)


SQUARES_180 = [square_mirror(sq) for sq in SQUARES]

# BitBoard

BitBoard = int
BB_SQUARES = [
    BB_A0, BB_B0, BB_C0, BB_D0, BB_E0, BB_F0, BB_G0, BB_H0, BB_I0,
    BB_A1, BB_B1, BB_C1, BB_D1, BB_E1, BB_F1, BB_G1, BB_H1, BB_I1,
    BB_A2, BB_B2, BB_C2, BB_D2, BB_E2, BB_F2, BB_G2, BB_H2, BB_I2,
    BB_A3, BB_B3, BB_C3, BB_D3, BB_E3, BB_F3, BB_G3, BB_H3, BB_I3,
    BB_A4, BB_B4, BB_C4, BB_D4, BB_E4, BB_F4, BB_G4, BB_H4, BB_I4,
    BB_A5, BB_B5, BB_C5, BB_D5, BB_E5, BB_F5, BB_G5, BB_H5, BB_I5,
    BB_A6, BB_B6, BB_C6, BB_D6, BB_E6, BB_F6, BB_G6, BB_H6, BB_I6,
    BB_A7, BB_B7, BB_C7, BB_D7, BB_E7, BB_F7, BB_G7, BB_H7, BB_I7,
    BB_A8, BB_B8, BB_C8, BB_D8, BB_E8, BB_F8, BB_G8, BB_H8, BB_I8,
    BB_A9, BB_B9, BB_C9, BB_D9, BB_E9, BB_F9, BB_G9, BB_H9, BB_I9
] = [1 << sq for sq in SQUARES]

BB_EMPTY = 0
BB_ALL = 0x3ffffffffffffffffffffff

BB_CORNERS = BB_A0 | BB_I0 | BB_A9 | BB_I9

BB_ROWS = [
    BB_ROW_0,
    BB_ROW_1,
    BB_ROW_2,
    BB_ROW_3,
    BB_ROW_4,
    BB_ROW_5,
    BB_ROW_6,
    BB_ROW_7,
    BB_ROW_8,
    BB_ROW_9
] = [0x1ff << (9 * i) for i in range(10)]

BB_COLUMNS = [
    BB_COLUMN_A,
    BB_COLUMN_B,
    BB_COLUMN_C,
    BB_COLUMN_D,
    BB_COLUMN_E,
    BB_COLUMN_F,
    BB_COLUMN_G,
    BB_COLUMN_H,
    BB_COLUMN_I
] = [0x201008040201008040201 << i for i in range(9)]

BB_COLOR_SIDES = [0x3ffffffffffe00000000000, 0x1fffffffffff]

BB_PALACES = [0x70381c0000000000000000, 0xe07038]
BB_ADVISOR_POS = [0x5010140000000000000000, 0xa02028]
BB_BISHOP_POS = [0x8800888008800000000000, 0x44004440044]
BB_PAWN_POS = [0x556abfffffffffff, 0x3fffffffffff55aa8000000]

BB_START_PAWNS = BB_A3 | BB_C3 | BB_E3 | BB_G3 | BB_I3 | BB_A6 | BB_C6 | BB_E6 | BB_G6 | BB_I6
BB_START_ROOKS = BB_CORNERS
BB_START_KNIGHTS = BB_B0 | BB_H0 | BB_B9 | BB_H9
BB_START_BISHOPS = BB_C0 | BB_G0 | BB_C9 | BB_G9
BB_START_ADVISORS = BB_D0 | BB_F0 | BB_D9 | BB_F9
BB_START_KINGS = BB_E0 | BB_E9
BB_START_CANNONS = BB_B2 | BB_H2 | BB_B7 | BB_H7

BB_START_OCCUPIED_RED = BB_ROW_0 | BB_A3 | BB_C3 | BB_E3 | BB_G3 | BB_I3 | BB_B2 | BB_H2
BB_START_OCCUPIED_BLACK = BB_ROW_9 | BB_A6 | BB_C6 | BB_E6 | BB_G6 | BB_I6 | BB_B7 | BB_H7
BB_START_OCCUPIED = BB_START_OCCUPIED_RED | BB_START_OCCUPIED_BLACK


def _sliding_attacks(square: Square, occupied: BitBoard, deltas: Iterable[int]):
    attacks = BB_EMPTY

    for delta in deltas:
        sq = square

        while True:
            sq += delta
            if not (0 <= sq < 90) or square_distance(sq, sq - delta) > 2:
                break

            attacks |= BB_SQUARES[sq]

            if occupied & BB_SQUARES[sq]:
                break

    return attacks


def _step_attacks(square: Square, deltas: Iterable[int], restriction: BitBoard = BB_ALL):
    if not BB_SQUARES[square] & restriction:
        return BB_EMPTY
    return restriction & _sliding_attacks(square, BB_ALL, deltas)


KNIGHT_LEG_DELTAS = [1, 9, -1, -9]
KNIGHT_ATTACK_DELTAS = [-7, 11, 17, 19, -11, 7, -19, -17]


def _knight_attacks(square: Square, occupied: BitBoard):
    attacks = BB_EMPTY

    for i, leg_delta in enumerate(KNIGHT_LEG_DELTAS):
        leg_sq = square + leg_delta
        if not (0 <= leg_sq < 90):
            continue
        if not occupied & BB_SQUARES[leg_sq]:
            attack_deltas = KNIGHT_ATTACK_DELTAS[2 * i: 2 * i + 2]
            for delta in attack_deltas:
                sq = square + delta
                if not (0 <= sq <= 90) or square_distance(sq, square) > 2:
                    continue
                attacks |= BB_SQUARES[sq]

    return attacks


KNIGHT_ATTACKER_LEG_DELTAS = [8, 10, -8, -10]
KNIGHT_ATTACKER_DELTAS = [7, 17, 19, 11, -7, -17, -19, -11]


def _knights_can_attack(square: Square, occupied: BitBoard):
    attackers = BB_EMPTY

    for i, leg_delta in enumerate(KNIGHT_ATTACKER_LEG_DELTAS):
        leg_sq = square + leg_delta
        if not (0 <= leg_sq < 90):
            continue
        if not occupied & BB_SQUARES[leg_sq]:
            attack_deltas = KNIGHT_ATTACKER_DELTAS[2 * i: 2 * i + 2]
            for delta in attack_deltas:
                sq = square + delta
                if not (0 <= sq <= 90) or square_distance(sq, square) > 2:
                    continue
                attackers |= BB_SQUARES[sq]

    return attackers


BISHOP_EYE_DELTAS = [8, -8, 10, -10]
BISHOP_ATTACK_DELTAS = [16, -16, 20, -20]


def _bishop_attacks(square: Square, occupied: BitBoard, color: int):
    attacks = BB_EMPTY

    for delta, leg_delta in zip(BISHOP_ATTACK_DELTAS, BISHOP_EYE_DELTAS):
        eye_sq = square + leg_delta
        if not (0 <= eye_sq < 90):
            continue
        if not occupied & BB_SQUARES[eye_sq]:
            sq = square + delta
            if not (0 <= sq <= 90) or square_distance(sq, square) > 2:
                continue
            attacks |= BB_SQUARES[sq]

    return attacks & BB_BISHOP_POS[color]


BB_PAWN_ATTACKS = [[], []]
BB_PAWN_ATTACKS[BLACK] = [_step_attacks(sq, [-9, -1, 1], BB_PAWN_POS[BLACK]) for sq in range(45)] + \
                         [_step_attacks(sq, [-9], BB_PAWN_POS[BLACK]) for sq in range(45, 90)]
BB_PAWN_ATTACKS[RED] = [_step_attacks(sq, [9], BB_PAWN_POS[RED]) for sq in range(45)] + \
                       [_step_attacks(sq, [9, -1, 1], BB_PAWN_POS[RED]) for sq in range(45, 90)]

BB_KING_ATTACKS = [[_step_attacks(sq, [9, -9, 1, -1], BB_PALACES[color]) for sq in SQUARES] for color in COLORS]
BB_ADVISOR_ATTACKS = [[_step_attacks(sq, [8, -8, 10, -10], BB_ADVISOR_POS[color]) for sq in SQUARES] for color in
                      COLORS]

BB_PAWNS_CAN_ATTACK = [[], []]
BB_PAWNS_CAN_ATTACK[BLACK] = [_step_attacks(sq, [9, -1, 1], BB_PAWN_POS[BLACK]) for sq in range(45)] + \
                             [_step_attacks(sq, [9], BB_PAWN_POS[BLACK]) for sq in range(45, 90)]
BB_PAWNS_CAN_ATTACK[RED] = [_step_attacks(sq, [-9], BB_PAWN_POS[RED]) for sq in range(45)] + \
                           [_step_attacks(sq, [-9, -1, 1], BB_PAWN_POS[RED]) for sq in range(45, 90)]


def _edges(square: Square) -> BitBoard:
    return (((BB_ROW_0 | BB_ROW_9) & ~BB_ROWS[square_row(square)]) |
            ((BB_COLUMN_A | BB_COLUMN_I) & ~BB_COLUMNS[square_column(square)]))


def _carry_rippler(mask: BitBoard) -> Iterator[BitBoard]:
    # Carry-Rippler trick to iterate subsets of mask.
    subset = BB_EMPTY
    while True:
        yield subset
        subset = (subset - mask) & mask
        if not subset:
            break


def _attack_table(deltas: List[int]) -> Tuple[List[BitBoard], List[Dict[BitBoard, BitBoard]]]:
    mask_table = []
    attack_table = []

    for square in SQUARES:
        attacks = {}

        mask = _sliding_attacks(square, 0, deltas) & ~_edges(square)
        for subset in _carry_rippler(mask):
            attacks[subset] = _sliding_attacks(square, subset, deltas)

        attack_table.append(attacks)
        mask_table.append(mask)

    return mask_table, attack_table


BB_COLUMN_MASKS, BB_COLUMN_ATTACKS = _attack_table([-9, 9])  # 车在某个位置时,该列上棋子各种分布对应的其能吃到的范围
BB_ROW_MASKS, BB_ROW_ATTACKS = _attack_table([-1, 1])  # 车在某个位置时,该行上棋子各种分布对应的其能吃到的范围


def _rook_attacks(square: Square, occupied: BitBoard):
    return _sliding_attacks(square, occupied, [1, -1, 9, -9])


def _cannon_attacks(square: Square, occupied: BitBoard):
    attacks = BB_EMPTY

    for delta in [1, -1, 9, -9]:
        sq = square
        occupied_num = 0

        while True:
            sq += delta
            if not (0 <= sq < 90) or square_distance(sq, sq - delta) > 2:
                break

            if occupied & BB_SQUARES[sq]:
                occupied_num += 1
                if occupied_num == 2:
                    attacks |= BB_SQUARES[sq]
                if occupied_num == 3:
                    break

    return attacks


def _cannon_slides(square: Square, occupied: BitBoard):
    slides = BB_EMPTY

    for delta in [1, -1, 9, -9]:
        sq = square

        while True:
            sq += delta
            if not (0 <= sq < 90) or square_distance(sq, sq - delta) > 2:
                break

            if occupied & BB_SQUARES[sq]:
                break
            slides |= BB_SQUARES[sq]

    return slides


def msb(bb: BitBoard):
    """Most Significant Byte"""
    return bb.bit_length() - 1


def lsb(bb: BitBoard):
    """Least Significant Byte"""
    return (bb & -bb).bit_length() - 1


def _lines() -> List[List[BitBoard]]:
    lines = []
    for a, bb_a in enumerate(BB_SQUARES):
        rays_row = []
        for b, bb_b in enumerate(BB_SQUARES):
            if BB_ROW_ATTACKS[a][0] & bb_b:
                rays_row.append(BB_ROW_ATTACKS[a][0] | bb_a)
            elif BB_COLUMN_ATTACKS[a][0] & bb_b:
                rays_row.append(BB_COLUMN_ATTACKS[a][0] | bb_a)
            else:
                rays_row.append(BB_EMPTY)
        lines.append(rays_row)
    return lines


BB_LINES = _lines()


def line(a: Square, b: Square) -> BitBoard:
    return BB_LINES[a][b]


def between(a: Square, b: Square):
    bb = BB_LINES[a][b] & ((BB_ALL << a) ^ (BB_ALL << b))
    return bb & (bb - 1)


class Piece:
    """A piece with type and color."""

    def __init__(self, piece_type: PieceType, color: Color):
        self.piece_type = piece_type
        """The piece type."""

        self.color = color
        """The piece color."""

    def symbol(self):
        symbol = piece_symbol(self.piece_type)
        return symbol.upper() if self.color else symbol

    def unicode_symbol(self, *, invert_color: bool = False):
        symbol = self.symbol().swapcase() if invert_color else self.symbol()
        return UNICODE_PIECE_SYMBOLS[symbol]

    def __hash__(self) -> int:
        return self.piece_type + (-1 if self.color else 5)

    def __repr__(self) -> str:
        return f"Piece.from_symbol({self.symbol()!r})"

    def __str__(self) -> str:
        return self.symbol()

    def _repr_svg_(self) -> str:
        import chess.svg
        return chess.svg.piece(self, size=45)

    @classmethod
    def from_symbol(cls, symbol: str):
        return cls(PIECE_SYMBOLS.index(symbol.lower()), symbol.isupper())


@dataclasses.dataclass(unsafe_hash=True)
class Move:
    def __init__(self, from_square: Square, to_square: Square):
        self.from_square = from_square
        self.to_square = to_square

    def _uci(self):
        return SQUARE_NAMES[self.from_square] + SQUARE_NAMES[self.to_square]

    def uci(self) -> str:
        """
        Gets a UCI string for the move.

        The UCI representation of a null move is ``0000``.
        """
        if self:
            return SQUARE_NAMES[self.from_square] + SQUARE_NAMES[self.to_square]
        else:
            return "0000"

    @classmethod
    def from_uci(cls, uci: str):
        if len(uci) == 4:
            from_square = SQUARE_NAMES.index(uci[0:2])
            to_square = SQUARE_NAMES.index(uci[2:4])
            return cls(from_square, to_square)
        else:
            raise ValueError(f"expected uci string to be of length 4: {uci!r}")

    def __repr__(self) -> str:
        return f"Move.from_uci({self.uci()!r})"

    def __str__(self) -> str:
        return self.uci()


class BaseBoard:
    def __init__(self, board_fen: Optional[str] = STARTING_BOARD_FEN):
        self.occupied_co = [BB_EMPTY, BB_EMPTY]
        if board_fen is None:
            self._clear_board()
        elif board_fen == STARTING_BOARD_FEN:
            self._reset_board()
        else:
            self._set_board_fen(board_fen)

    def _clear_board(self):
        self.pawns = BB_EMPTY
        self.rooks = BB_EMPTY
        self.knights = BB_EMPTY
        self.bishops = BB_EMPTY
        self.advisors = BB_EMPTY
        self.kings = BB_EMPTY
        self.cannons = BB_EMPTY

        self.occupied_co[RED] = BB_EMPTY
        self.occupied_co[BLACK] = BB_EMPTY
        self.occupied = BB_EMPTY

    def clear_board(self):
        self._clear_board()

    def _reset_board(self):
        self.pawns = BB_START_PAWNS
        self.rooks = BB_START_ROOKS
        self.knights = BB_START_KNIGHTS
        self.bishops = BB_START_BISHOPS
        self.advisors = BB_START_ADVISORS
        self.kings = BB_START_KINGS
        self.cannons = BB_START_CANNONS

        self.occupied_co[RED] = BB_START_OCCUPIED_RED
        self.occupied_co[BLACK] = BB_START_OCCUPIED_BLACK
        self.occupied = BB_START_OCCUPIED

    def reset_board(self):
        self._reset_board()

    def _repr_svg_(self):
        import cchess.svg
        return cchess.svg.board(board=self, size=600)

    def _set_board_fen(self, fen: str):
        # Compatibility with set_fen().
        fen = fen.strip()
        if " " in fen:
            raise ValueError(f"expected position part of fen, got multiple parts: {fen!r}")

        # Ensure the FEN is valid.
        rows = fen.split("/")
        if len(rows) != 10:
            raise ValueError(f"expected 10 rows in position part of fen: {fen!r}")

        # Validate each row.
        for row in rows:
            field_sum = 0
            previous_was_digit = False

            for c in row:
                if c in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    if previous_was_digit:
                        raise ValueError(f"two subsequent digits in position part of fen: {fen!r}")
                    field_sum += int(c)
                    previous_was_digit = True
                elif c.lower() in PIECE_SYMBOLS:
                    field_sum += 1
                    previous_was_digit = False
                else:
                    raise ValueError(f"invalid character in position part of fen: {fen!r}")

            if field_sum != 9:
                raise ValueError(f"expected 9 columns per row in position part of fen: {fen!r}")

        # Clear the board.
        self._clear_board()

        # Put pieces on the board.
        square_index = 0
        for c in fen:
            if c in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                square_index += int(c)
            elif c.lower() in PIECE_SYMBOLS:
                piece = Piece.from_symbol(c)
                self._set_piece_at(SQUARES_180[square_index], piece.piece_type, piece.color)
                square_index += 1

    def set_board_fen(self, fen: str):
        """
        Parses *fen* and sets up the board, where *fen* is the board part of
        a FEN.

        :raises: :exc:`ValueError` if syntactically invalid.
        """
        self._set_board_fen(fen)

    def piece_map(self, *, mask: BitBoard = BB_ALL):
        """
        Gets a dictionary of :class:`pieces <chess.Piece>` by square index.
        """
        result = {}
        for square in scan_reversed(self.occupied & mask):
            result[square] = self.piece_at(square)
        return result

    def _set_piece_map(self, pieces: Dict[Square, Piece]) -> None:
        self._clear_board()
        for square, piece in pieces.items():
            self._set_piece_at(square, piece.piece_type, piece.color)

    def set_piece_map(self, pieces: Dict[Square, Piece]) -> None:
        """
        Sets up the board from a dictionary of :class:`pieces <chess.Piece>`
        by square index.
        """
        self._set_piece_map(pieces)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.board_fen()!r})"

    def __str__(self) -> str:
        builder = []

        for square in SQUARES_180:
            piece = self.piece_at(square)

            if piece:
                builder.append(piece.symbol())
            else:
                builder.append(".")

            if BB_SQUARES[square] & BB_COLUMN_I:
                if square != I0:
                    builder.append("\n")
            else:
                builder.append(" ")

        return "".join(builder)

    def unicode(self, *, invert_color: bool = False, axes: bool = True) -> str:
        """
        Returns a string representation of the board with Unicode pieces.
        Useful for pretty-printing to a terminal.

        :param invert_color: Invert color of the Unicode pieces.
        :param axes: Show a coordinate axes margin.
        """
        builder = []
        if axes:
            builder.append('  ａｂｃｄｅｆｇｈｉ\n')

        for row_index in range(9, -1, -1):
            if axes:
                builder.append(ROW_NAMES[row_index])
                builder.append(' ')

            for col_index in range(9):
                square_index = square(col_index, row_index)

                piece = self.piece_at(square_index)

                if piece:
                    builder.append(piece.unicode_symbol(invert_color=invert_color))
                else:
                    builder.append("．")

            if axes or row_index > 0:
                builder.append("\n")

        if axes:
            builder.append('  ａｂｃｄｅｆｇｈｉ')

        return "".join(builder)

    def pieces_mask(self, piece_type: PieceType, color: Color) -> BitBoard:
        if piece_type == PAWN:
            bb = self.pawns
        elif piece_type == ROOK:
            bb = self.rooks
        elif piece_type == KNIGHT:
            bb = self.knights
        elif piece_type == BISHOP:
            bb = self.bishops
        elif piece_type == ADVISOR:
            bb = self.advisors
        elif piece_type == KING:
            bb = self.kings
        elif piece_type == CANNON:
            bb = self.cannons
        else:
            assert False, f"expected PieceType, got {piece_type!r}"

        return bb & self.occupied_co[color]

    def piece_at(self, square: Square):
        """Gets the :class:`piece <chess.Piece>` at the given square."""
        piece_type = self.piece_type_at(square)
        if piece_type:
            mask = BB_SQUARES[square]
            color = bool(self.occupied_co[RED] & mask)
            return Piece(piece_type, color)
        else:
            return None

    def piece_type_at(self, square: Square):
        mask = BB_SQUARES[square]

        if not self.occupied & mask:
            return None
        elif self.pawns & mask:
            return PAWN
        elif self.rooks & mask:
            return ROOK
        elif self.knights & mask:
            return KNIGHT
        elif self.bishops & mask:
            return BISHOP
        elif self.advisors & mask:
            return ADVISOR
        elif self.kings & mask:
            return KING
        else:
            return CANNON

    def color_at(self, square: Square):
        """Gets the color of the piece at the given square."""
        mask = BB_SQUARES[square]
        if self.occupied_co[RED] & mask:
            return RED
        elif self.occupied_co[BLACK] & mask:
            return BLACK
        else:
            return None

    def king(self, color: Color):
        """
        Finds the king square of the given side. Returns ``None`` if there
        is no king of that color.
        """
        king_mask = self.occupied_co[color] & self.kings
        return msb(king_mask) if king_mask else None

    def attacks_mask(self, square: Square) -> BitBoard:
        bb_square = BB_SQUARES[square]

        if bb_square & self.pawns:
            color = bool(bb_square & self.occupied_co[RED])
            return BB_PAWN_ATTACKS[color][square]
        elif bb_square & self.rooks:
            return _rook_attacks(square, self.occupied)
        elif bb_square & self.knights:
            return _knight_attacks(square, self.occupied)
        elif bb_square & self.bishops:
            color = bool(bb_square & self.occupied_co[RED])
            return _bishop_attacks(square, self.occupied, color)
        elif bb_square & self.advisors:
            color = bool(bb_square & self.occupied_co[RED])
            return BB_ADVISOR_ATTACKS[color][square]
        elif bb_square & self.kings:
            color = bool(bb_square & self.occupied_co[RED])
            return BB_KING_ATTACKS[color][square]
        elif bb_square & self.cannons:
            return _cannon_attacks(square, self.occupied)
        return 0

    def attacks(self, square: Square):
        """
        Gets the set of attacked squares from the given square.

        There will be no attacks if the square is empty. Pinned pieces are
        still attacking other squares.

        Returns a :class:`set of squares <chess.SquareSet>`.
        """
        return SquareSet(self.attacks_mask(square))

    def _attackers_mask(self, color: Color, square: Square, occupied: BitBoard) -> BitBoard:
        row_pieces = BB_ROW_MASKS[square] & occupied
        column_pieces = BB_COLUMN_MASKS[square] & occupied

        attackers = (
                (BB_ROW_ATTACKS[square][row_pieces] & self.rooks) |
                (BB_COLUMN_ATTACKS[square][column_pieces] & self.rooks) |
                _knights_can_attack(square, occupied) & self.knights |
                _bishop_attacks(square, occupied, color) & self.bishops |
                BB_ADVISOR_ATTACKS[color][square] & self.advisors |
                BB_KING_ATTACKS[color][square] & self.kings |
                BB_PAWNS_CAN_ATTACK[color][square] & self.pawns |
                _cannon_attacks(square, occupied) & self.cannons
        )

        return attackers & self.occupied_co[color]

    def attackers_mask(self, color: Color, square: Square) -> BitBoard:
        return self._attackers_mask(color, square, self.occupied)

    def is_attacked_by(self, color: Color, square: Square) -> bool:
        """
        Checks if the given side attacks the given square.

        Pinned pieces still count as attackers. Pawns that can be captured
        en passant are **not** considered attacked.
        """
        return bool(self.attackers_mask(color, square))

    def attackers(self, color: Color, square: Square):
        """
        Gets the set of attackers of the given color for the given square.

        Pinned pieces still count as attackers.

        Returns a :class:`set of squares <chess.SquareSet>`.
        """
        return SquareSet(self.attackers_mask(color, square))

    def _remove_piece_at(self, square: Square):
        piece_type = self.piece_type_at(square)
        mask = BB_SQUARES[square]

        if piece_type == PAWN:
            self.pawns ^= mask
        elif piece_type == ROOK:
            self.rooks ^= mask
        elif piece_type == KNIGHT:
            self.knights ^= mask
        elif piece_type == BISHOP:
            self.bishops ^= mask
        elif piece_type == ADVISOR:
            self.advisors ^= mask
        elif piece_type == KING:
            self.kings ^= mask
        elif piece_type == CANNON:
            self.cannons ^= mask
        else:
            return None

        self.occupied ^= mask
        self.occupied_co[RED] &= ~mask
        self.occupied_co[BLACK] &= ~mask

        return piece_type

    def remove_piece_at(self, square: Square):
        color = bool(self.occupied_co[RED] & BB_SQUARES[square])
        piece_type = self._remove_piece_at(square)
        return Piece(piece_type, color) if piece_type else None

    def _set_piece_at(self, square: Square, piece_type: PieceType, color: Color):
        self._remove_piece_at(square)

        mask = BB_SQUARES[square]

        if piece_type == PAWN:
            self.pawns |= mask
        elif piece_type == ROOK:
            self.rooks |= mask
        elif piece_type == KNIGHT:
            self.knights |= mask
        elif piece_type == BISHOP:
            self.bishops |= mask
        elif piece_type == ADVISOR:
            self.advisors |= mask
        elif piece_type == KING:
            self.kings |= mask
        elif piece_type == CANNON:
            self.cannons |= mask
        else:
            return

        self.occupied |= mask
        self.occupied_co[color] |= mask

    def set_piece_at(self, square: Square, piece):
        if piece is None:
            self._remove_piece_at(square)
        else:
            self._set_piece_at(square, piece.piece_type, piece.color)

    def board_fen(self) -> str:
        """
        Gets the board FEN (e.g.,
        ``rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR``).
        """
        builder = []
        empty = 0

        for square in SQUARES_180:
            piece = self.piece_at(square)

            if not piece:
                empty += 1
            else:
                if empty:
                    builder.append(str(empty))
                    empty = 0
                builder.append(piece.symbol())

            if BB_SQUARES[square] & BB_COLUMN_I:
                if empty:
                    builder.append(str(empty))
                    empty = 0

                if square != I0:
                    builder.append("/")

        return "".join(builder)

    def __eq__(self, board: object) -> bool:
        if isinstance(board, BaseBoard):
            return (
                    self.occupied == board.occupied and
                    self.occupied_co[RED] == board.occupied_co[RED] and
                    self.pawns == board.pawns and
                    self.rooks == board.rooks and
                    self.knights == board.knights and
                    self.bishops == board.bishops and
                    self.advisors == board.advisors and
                    self.kings == board.kings and
                    self.cannons == board.cannons)
        else:
            return NotImplemented

    def copy(self):
        """Creates a copy of the board."""
        board = type(self)(None)

        board.pawns = self.pawns
        board.knights = self.knights
        board.rooks = self.rooks
        board.bishops = self.bishops
        board.advisors = self.advisors
        board.kings = self.kings
        board.cannons = self.cannons

        board.occupied_co[RED] = self.occupied_co[RED]
        board.occupied_co[BLACK] = self.occupied_co[BLACK]
        board.occupied = self.occupied

        return board

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo: Dict[int, object]):
        board = self.copy()
        memo[id(self)] = board
        return board

    @classmethod
    def empty(cls):
        """
        Creates a new empty board. Also see
        :func:`~chess.BaseBoard.clear_board()`.
        """
        return cls(None)


class _BoardState:

    def __init__(self, board) -> None:
        self.pawns = board.pawns
        self.rooks = board.rooks
        self.knights = board.knights
        self.bishops = board.bishops
        self.advisors = board.advisors
        self.kings = board.kings
        self.cannons = board.cannons

        self.occupied_r = board.occupied_co[RED]
        self.occupied_b = board.occupied_co[BLACK]
        self.occupied = board.occupied

        self.turn = board.turn
        self.halfmove_clock = board.halfmove_clock
        self.fullmove_number = board.fullmove_number

    def restore(self, board) -> None:
        board.pawns = self.pawns
        board.rooks = self.rooks
        board.knights = self.knights
        board.bishops = self.bishops
        board.advisors = self.advisors
        board.kings = self.kings
        board.cannons = self.cannons

        board.occupied_co[RED] = self.occupied_r
        board.occupied_co[BLACK] = self.occupied_b
        board.occupied = self.occupied

        board.turn = self.turn
        board.halfmove_clock = self.halfmove_clock
        board.fullmove_number = self.fullmove_number


class Board(BaseBoard):
    starting_fen = STARTING_FEN
    turn: Color
    """The side to move (``chess.RED`` or ``chess.BLACK``)."""
    fullmove_number: int
    """
    Counts move pairs. Starts at `1` and is incremented after every move
    of the black side.
    """
    halfmove_clock: int
    """The number of half-moves since the last capture or pawn move."""
    move_stack: List[Move]
    """
    The move stack. Use :func:`Board.push() <chess.Board.push()>`,
    :func:`Board.pop() <chess.Board.pop()>`,
    :func:`Board.peek() <chess.Board.peek()>` and
    :func:`Board.clear_stack() <chess.Board.clear_stack()>` for
    manipulation.
    """

    def __init__(self, fen: Optional[str] = STARTING_FEN):
        super(Board, self).__init__(None)
        self.move_stack = []
        self._stack = []

        if fen is None:
            self.clear()
        elif fen == type(self).starting_fen:
            self.reset()
        else:
            self.set_fen(fen)

    def __repr__(self):
        return f"{type(self).__name__}({self.fen()!r})"

    def _repr_svg_(self) -> str:
        import cchess.svg
        return cchess.svg.board(
            board=self,
            size=600,
            lastmove=self.peek() if self.move_stack else None,
            checkers=self.checkers() if self.is_check() else None)

    def fen(self) -> str:
        """
        Gets a FEN representation of the position.

        A FEN string (e.g.,
        ``rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR r - - 0 1``) consists
        of the board part :func:`~chess.Board.board_fen()`, the
        :data:`~chess.Board.turn`,
        the :data:`~chess.Board.halfmove_clock`
        and the :data:`~chess.Board.fullmove_number`.
        """
        return " ".join([
            self.epd(),
            str(self.halfmove_clock),
            str(self.fullmove_number)
        ])

    def epd(self) -> str:
        """
        Gets an EPD representation of the current position.
        """
        epd = [self.board_fen(),
               "r" if self.turn == RED else "b",
               '-', "-"]

        return " ".join(epd)

    def set_fen(self, fen: str) -> None:
        """
        Parses a FEN and sets the position from it.

        :raises: :exc:`ValueError` if syntactically invalid. Use
            :func:`~chess.Board.is_valid()` to detect invalid positions.
        """
        parts = fen.split()

        # Board part.
        try:
            board_part = parts.pop(0)
        except IndexError:
            raise ValueError("empty fen")

        # Turn.
        try:
            turn_part = parts.pop(0)
        except IndexError:
            turn = RED
        else:
            if turn_part == "w":
                turn = RED
            elif turn_part == "b":
                turn = BLACK
            else:
                raise ValueError(f"expected 'w' or 'b' for turn part of fen: {fen!r}")

        try:
            parts.pop(0)
        except IndexError:
            pass
        try:
            parts.pop(0)
        except IndexError:
            pass

        # Check that the half-move part is valid.
        try:
            halfmove_part = parts.pop(0)
        except IndexError:
            halfmove_clock = 0
        else:
            try:
                halfmove_clock = int(halfmove_part)
            except ValueError:
                raise ValueError(f"invalid half-move clock in fen: {fen!r}")

            if halfmove_clock < 0:
                raise ValueError(f"half-move clock cannot be negative: {fen!r}")

        # Check that the full-move number part is valid.
        # 0 is allowed for compatibility, but later replaced with 1.
        try:
            fullmove_part = parts.pop(0)
        except IndexError:
            fullmove_number = 1
        else:
            try:
                fullmove_number = int(fullmove_part)
            except ValueError:
                raise ValueError(f"invalid fullmove number in fen: {fen!r}")

            if fullmove_number < 0:
                raise ValueError(f"fullmove number cannot be negative: {fen!r}")

            fullmove_number = max(fullmove_number, 1)

        # All parts should be consumed now.
        if parts:
            raise ValueError(f"fen string has more parts than expected: {fen!r}")

        # Validate the board part and set it.
        self._set_board_fen(board_part)

        # Apply.
        self.turn = turn
        self.halfmove_clock = halfmove_clock
        self.fullmove_number = fullmove_number
        self.clear_stack()

    @property
    def legal_moves(self):
        """
        A dynamic list of legal moves.
        """
        return LegalMoveGenerator(self)

    @property
    def pseudo_legal_moves(self):
        """
        A dynamic list of pseudo-legal moves, much like the legal move list.
        """
        return PseudoLegalMoveGenerator(self)

    def clear(self):
        """
        Clears the board.

        Resets move stack and move counters. The side to move is red.

        In order to be in a valid :func:`~chess.Board.status()`, at least kings
        need to be put on the board.
        """
        self.turn = RED
        self.halfmove_clock = 0
        self.fullmove_number = 1

        self.clear_board()

    def clear_board(self):
        super().clear_board()
        self.clear_stack()

    def clear_stack(self):
        """Clears the move stack."""
        self.move_stack.clear()
        self._stack.clear()

    def reset(self) -> None:
        """Restores the starting position."""
        self.turn = RED
        self.halfmove_clock = 0
        self.fullmove_number = 1

        self.reset_board()

    def reset_board(self) -> None:
        """
        Resets only pieces to the starting position. Use
        :func:`~chess.Board.reset()` to fully restore the starting position
        (including turn, castling rights, etc.).
        """
        super().reset_board()
        self.clear_stack()

    def root(self):
        """Returns a copy of the root position."""
        if self._stack:
            board = type(self)(None)
            self._stack[0].restore(board)
            return board
        else:
            return self.copy(stack=False)

    def copy(self, *, stack: Union[bool, int] = True):
        """
        Creates a copy of the board.

        Defaults to copying the entire move stack. Alternatively, *stack* can
        be ``False``, or an integer to copy a limited number of moves.
        """
        board = super().copy()

        board.turn = self.turn
        board.fullmove_number = self.fullmove_number
        board.halfmove_clock = self.halfmove_clock

        if stack:
            stack = len(self.move_stack) if stack is True else stack
            board.move_stack = [copy.copy(move) for move in self.move_stack[-stack:]]
            board._stack = self._stack[-stack:]

        return board

    @classmethod
    def empty(cls):
        """Creates a new empty board. Also see :func:`~chess.Board.clear()`."""
        return cls(None)

    def ply(self) -> int:
        return 2 * (self.fullmove_number - 1) + (self.turn == BLACK)

    def remove_piece_at(self, square: Square, clear_stack=True):
        piece = super().remove_piece_at(square)
        if clear_stack:
            self.clear_stack()
        return piece

    def set_piece_at(self, square: Square, piece: Optional[Piece], clear_stack=True):
        super().set_piece_at(square, piece)
        if clear_stack:
            self.clear_stack()

    def checkers_mask(self) -> BitBoard:
        king = self.king(self.turn)
        return BB_EMPTY if king is None else self.attackers_mask(not self.turn, king)

    def checkers(self):
        """
        Gets the pieces currently giving check.

        Returns a :class:`set of squares <chess.SquareSet>`.
        """
        return SquareSet(self.checkers_mask())

    def is_check(self) -> bool:
        """Tests if the current side to move is in check."""
        return bool(self.checkers_mask())

    def is_white_face(self) -> bool:
        red_king, black_king = self.king(RED), self.king(BLACK)
        if red_king is None or black_king is None:
            return False
        between_kings = between(red_king, black_king)
        if not between_kings:
            return False
        return not bool(between(red_king, black_king) & self.occupied)

    def gives_check(self, move: Move) -> bool:
        """
        Probes if the given move would put the opponent in check. The move
        must be at least pseudo-legal.
        """
        self.push(move)
        try:
            return self.is_check()
        finally:
            self.pop()

    def _is_safe(self, move: Move) -> bool:
        try:
            self.push(move)
            return not (bool(self.attackers_mask(self.turn, self.king(not self.turn))) | self.is_white_face())
        finally:
            self.pop()

    def generate_pseudo_legal_moves(self, from_mask: BitBoard = BB_ALL, to_mask: BitBoard = BB_ALL) -> Iterator[Move]:
        our_pieces = self.occupied_co[self.turn]

        for from_square in scan_reversed(our_pieces & from_mask):
            moves = self.attacks_mask(from_square) & ~our_pieces & to_mask
            for to_square in scan_reversed(moves):
                yield Move(from_square, to_square)  # pieces attack
            if BB_SQUARES[from_square] & self.cannons:
                slides = _cannon_slides(from_square, self.occupied) & to_mask
                for to_square in scan_reversed(slides):
                    yield Move(from_square, to_square)  # cannons slide

    def generate_pseudo_legal_captures(self, from_mask: BitBoard = BB_ALL, to_mask: BitBoard = BB_ALL) -> Iterator[
        Move]:
        return self.generate_pseudo_legal_moves(from_mask, to_mask & self.occupied_co[not self.turn])

    def generate_legal_moves(self, from_mask: BitBoard = BB_ALL, to_mask: BitBoard = BB_ALL) -> Iterator[Move]:

        king = self.king(self.turn)
        oppo_king = self.king(not self.turn)
        if king:
            for move in self.generate_pseudo_legal_moves(from_mask, to_mask):
                if move.to_square == oppo_king:
                    yield move
                elif self._is_safe(move):
                    yield move
        else:
            yield from self.generate_pseudo_legal_moves(from_mask, to_mask)

    def generate_legal_captures(self, from_mask: BitBoard = BB_ALL, to_mask: BitBoard = BB_ALL) -> Iterator[Move]:
        return self.generate_legal_moves(from_mask, to_mask & self.occupied_co[not self.turn])

    def is_into_check(self, move):
        king = self.king(self.turn)
        if king is None:
            return False
        return not self._is_safe(move)

    def was_into_check(self) -> bool:
        king = self.king(not self.turn)
        return king is not None and self.is_attacked_by(self.turn, king)

    def is_pseudo_legal(self, move: Move) -> bool:
        # Null moves are not pseudo-legal.
        if not move:
            return False

        # Source square must not be vacant.
        piece = self.piece_type_at(move.from_square)
        if not piece:
            return False

        # Get square masks.
        from_mask = BB_SQUARES[move.from_square]
        to_mask = BB_SQUARES[move.to_square]

        # Check turn.
        if not self.occupied_co[self.turn] & from_mask:
            return False

        # Destination square can not be occupied by own piece.
        if self.occupied_co[self.turn] & to_mask:
            return False

        # Cannon
        if piece == CANNON:
            slides = _cannon_slides(move.from_square, self.occupied)
            if to_mask & slides:
                return True

        # Handle all other pieces.
        return bool(self.attacks_mask(move.from_square) & to_mask)

    def is_legal(self, move: Move) -> bool:
        if self.is_pseudo_legal(move):
            if move.to_square == self.king(not self.turn):
                return True
            return not self.is_into_check(move)
        return False

    def _board_state(self):
        return _BoardState(self)

    def is_zeroing(self, move: Move) -> bool:
        """Checks if the given pseudo-legal move is a capture."""
        to_square = BB_SQUARES[move.to_square]
        return bool(to_square & self.occupied_co[not self.turn])

    def push(self, move: Move) -> None:
        """
        Updates the position with the given *move* and puts it onto the
        move stack.

        Null moves just increment the move counters, switch turns.

        .. warning::
            Moves are not checked for legality. It is the caller's
            responsibility to ensure that the move is at least pseudo-legal or
            a null move.
        """
        # Push move and remember board state.
        board_state = self._board_state()
        self.move_stack.append(move)
        self._stack.append(board_state)

        # Increment move counters.
        self.halfmove_clock += 1
        if self.turn == BLACK:
            self.fullmove_number += 1

        # Zero the half-move clock.
        if self.is_zeroing(move):
            self.halfmove_clock = 0

        piece = self.remove_piece_at(move.from_square, clear_stack=False)
        assert piece is not None, f"push() expects move to be pseudo-legal, but got {move} in {self.board_fen()}"
        self.set_piece_at(move.to_square, piece, clear_stack=False)

        # Swap turn.
        self.turn = not self.turn

    def pop(self) -> Move:
        """
        Restores the previous position and returns the last move from the stack.

        :raises: :exc:`IndexError` if the move stack is empty.
        """
        move = self.move_stack.pop()
        self._stack.pop().restore(self)
        return move

    def peek(self) -> Move:
        """
        Gets the last move from the move stack.

        :raises: :exc:`IndexError` if the move stack is empty.
        """
        return self.move_stack[-1]

    def find_move(self, from_square: Square, to_square: Square) -> Move:
        """
        Finds a matching legal move for an origin square and a target square.

        :raises: :exc:`ValueError` if no matching legal move is found.
        """

        move = Move(from_square=from_square, to_square=to_square)
        if not self.is_legal(move):
            raise ValueError(
                f"no matching legal move for {move.uci()} ({SQUARE_NAMES[from_square]} -> {SQUARE_NAMES[to_square]}) in {self.fen()}")

        return move

    def is_checkmate(self) -> bool:
        """Checks if the current position is a checkmate."""
        if not self.is_check():
            return False

        return not any(self.generate_legal_moves())

    def is_stalemate(self) -> bool:
        """Checks if the current position is a stalemate."""
        if self.is_check():
            return False

        return not any(self.generate_legal_moves())

    def _is_halfmoves(self, n: int) -> bool:
        return self.halfmove_clock >= n and any(self.generate_legal_moves())

    def is_forty_moves(self) -> bool:
        return self._is_halfmoves(80)

    def is_fifty_moves(self) -> bool:
        return self._is_halfmoves(100)

    def is_sixty_moves(self) -> bool:
        return self._is_halfmoves(120)

    def _transposition_key(self):
        return (self.pawns, self.rooks, self.knights, self.bishops,
                self.advisors, self.kings, self.cannons,
                self.occupied_co[RED], self.occupied_co[BLACK],
                self.turn)

    def is_irreversible(self, move: Move) -> bool:
        return self.is_zeroing(move)

    def is_repetition(self, count: int = 3) -> bool:
        """
        Checks if the current position has repeated 3 (or a given number of)
        times.

        Unlike :func:`~chess.Board.can_claim_threefold_repetition()`,
        this does not consider a repetition that can be played on the next
        move.

        Note that checking this can be slow: In the worst case, the entire
        game has to be replayed because there is no incremental transposition
        table.
        """
        # Fast check, based on occupancy only.
        maybe_repetitions = 1
        for state in reversed(self._stack):
            if state.occupied == self.occupied:
                maybe_repetitions += 1
                if maybe_repetitions >= count:
                    break
        if maybe_repetitions < count:
            return False

        # Check full replay.
        transposition_key = self._transposition_key()
        switchyard = []

        try:
            while True:
                if count <= 1:
                    return True

                if len(self.move_stack) < count - 1:
                    break

                move = self.pop()
                switchyard.append(move)

                if self.is_irreversible(move):
                    break

                if self._transposition_key() == transposition_key:
                    count -= 1
        finally:
            while switchyard:
                self.push(switchyard.pop())

        return False

    def is_fivefold_repetition(self) -> bool:
        return self.is_repetition(5)

    def is_capture(self, move: Move) -> bool:
        touched = BB_SQUARES[move.from_square] ^ BB_SQUARES[move.to_square]
        return bool(touched & self.occupied_co[not self.turn])

    def status(self) -> Status:
        """
        Gets a bitmask of possible problems with the position.

        :data:`~chess.STATUS_VALID` if all basic validity requirements are met.
        This does not imply that the position is actually reachable with a
        series of legal moves from the starting position.
        """
        errors = STATUS_VALID

        # There must be at least one piece.
        if not self.occupied:
            errors |= STATUS_EMPTY

        # There can not be more than 16 pieces of any color.
        if popcount(self.occupied_co[RED]) > 16:
            errors |= STATUS_TOO_MANY_RED_PIECES
        if popcount(self.occupied_co[BLACK]) > 16:
            errors |= STATUS_TOO_MANY_BLACK_PIECES

        # There must be exactly one king of each color.
        if not self.occupied_co[RED] & self.kings:
            errors |= STATUS_NO_RED_KING
        if not self.occupied_co[BLACK] & self.kings:
            errors |= STATUS_NO_BLACK_KING
        # There can not be more than 1 king of any color.
        if popcount(self.occupied_co[RED] & self.kings) > 1:
            errors |= STATUS_TOO_MANY_RED_KINGS
        if popcount(self.occupied_co[BLACK] & self.kings) > 1:
            errors |= STATUS_TOO_MANY_BLACK_KINGS

        # Kings are placed on wrong places.
        if self.kings & self.occupied_co[RED] & ~BB_PALACES[RED]:
            errors |= STATUS_RED_KING_PLACE_WRONG
        if self.kings & self.occupied_co[BLACK] & ~BB_PALACES[BLACK]:
            errors |= STATUS_BLACK_KING_PLACE_WRONG

        # There can not be more than 5 pawns of any color.
        if popcount(self.occupied_co[RED] & self.pawns) > 5:
            errors |= STATUS_TOO_MANY_RED_PAWNS
        if popcount(self.occupied_co[BLACK] & self.pawns) > 5:
            errors |= STATUS_TOO_MANY_BLACK_PAWNS

        # Pawns are placed on wrong places.
        if self.pawns & self.occupied_co[RED] & ~BB_PAWN_POS[RED]:
            errors |= STATUS_RED_PAWNS_PLACE_WRONG
        if self.pawns & self.occupied_co[BLACK] & ~BB_PAWN_POS[BLACK]:
            errors |= STATUS_BLACK_PAWNS_PLACE_WRONG

        # There can not be more than 2 rooks of any color.
        if popcount(self.occupied_co[RED] & self.rooks) > 2:
            errors |= STATUS_TOO_MANY_RED_ROOKS
        if popcount(self.occupied_co[BLACK] & self.rooks) > 2:
            errors |= STATUS_TOO_MANY_BLACK_ROOKS

        # There can not be more than 2 knights of any color.
        if popcount(self.occupied_co[RED] & self.knights) > 2:
            errors |= STATUS_TOO_MANY_RED_KNIGHTS
        if popcount(self.occupied_co[BLACK] & self.knights) > 2:
            errors |= STATUS_TOO_MANY_BLACK_KNIGHTS

        # There can not be more than 2 bishops of any color.
        if popcount(self.occupied_co[RED] & self.bishops) > 2:
            errors |= STATUS_TOO_MANY_RED_BISHOPS
        if popcount(self.occupied_co[BLACK] & self.bishops) > 2:
            errors |= STATUS_TOO_MANY_BLACK_BISHOPS

        # Bishops are placed on wrong places.
        if self.bishops & self.occupied_co[RED] & ~BB_BISHOP_POS[RED]:
            errors |= STATUS_RED_BISHOPS_PLACE_WRONG
        if self.bishops & self.occupied_co[BLACK] & ~BB_BISHOP_POS[BLACK]:
            errors |= STATUS_BLACK_BISHOPS_PLACE_WRONG

        # There can not be more than 2 advisors of any color.
        if popcount(self.occupied_co[RED] & self.advisors) > 2:
            errors |= STATUS_TOO_MANY_RED_ADVISORS
        if popcount(self.occupied_co[BLACK] & self.advisors) > 2:
            errors |= STATUS_TOO_MANY_BLACK_ADVISORS

        # Advisors are placed on wrong places.
        if self.advisors & self.occupied_co[RED] & ~BB_ADVISOR_POS[RED]:
            errors |= STATUS_RED_ADVISORS_PLACE_WRONG
        if self.advisors & self.occupied_co[BLACK] & ~BB_ADVISOR_POS[BLACK]:
            errors |= STATUS_BLACK_ADVISORS_PLACE_WRONG

        # There can not be more than 2 cannons of any color.
        if popcount(self.occupied_co[RED] & self.cannons) > 2:
            errors |= STATUS_TOO_MANY_RED_CANNONS
        if popcount(self.occupied_co[BLACK] & self.cannons) > 2:
            errors |= STATUS_TOO_MANY_BLACK_CANNONS

        # Side to move giving check.
        if self.was_into_check():
            errors |= STATUS_OPPOSITE_CHECK

        return errors

    def is_valid(self) -> bool:
        """
        Checks some basic validity requirements.

        See :func:`~chess.Board.status()` for details.
        """
        return self.status() == STATUS_VALID


IntoSquareSet = Union[SupportsInt, Iterable[Square]]


def scan_forward(bb: BitBoard) -> Iterator[Square]:
    while bb:
        r = bb & -bb
        yield r.bit_length() - 1
        bb ^= r


def scan_reversed(bb: BitBoard) -> Iterator[Square]:
    while bb:
        r = bb.bit_length() - 1
        yield r
        bb ^= BB_SQUARES[r]


popcount: Callable[[BitBoard], int] = lambda x: bin(x).count('1')


class LegalMoveGenerator:

    def __init__(self, board: Board) -> None:
        self.board = board

    def __bool__(self) -> bool:
        return any(self.board.generate_legal_moves())

    def count(self) -> int:
        # List conversion is faster than iterating.
        return len(list(self))

    def __iter__(self) -> Iterator[Move]:
        return self.board.generate_legal_moves()

    def __contains__(self, move: Move) -> bool:
        return self.board.is_legal(move)

    def __repr__(self) -> str:
        sans = ", ".join(move.uci() for move in self)
        return f"<LegalMoveGenerator at {id(self):#x} ({sans})>"


class PseudoLegalMoveGenerator:

    def __init__(self, board: Board) -> None:
        self.board = board

    def __bool__(self) -> bool:
        return any(self.board.generate_pseudo_legal_moves())

    def count(self) -> int:
        # List conversion is faster than iterating.
        return len(list(self))

    def __iter__(self) -> Iterator[Move]:
        return self.board.generate_pseudo_legal_moves()

    def __contains__(self, move: Move) -> bool:
        return self.board.is_pseudo_legal(move)

    def __repr__(self) -> str:
        builder = []

        for move in self:
            builder.append(move.uci())

        sans = ", ".join(builder)
        return f"<PseudoLegalMoveGenerator at {id(self):#x} ({sans})>"


class SquareSet:

    def __init__(self, squares: IntoSquareSet = BB_EMPTY):
        try:
            self.mask = int(squares) & BB_ALL  # type: ignore
            return
        except TypeError:
            self.mask = 0
        for square in squares:
            self.add(square)

    def __contains__(self, square: Square) -> bool:
        return bool(BB_SQUARES[square] & self.mask)

    def __iter__(self) -> Iterator[Square]:
        return scan_forward(self.mask)

    def __reversed__(self) -> Iterator[Square]:
        return scan_reversed(self.mask)

    def __len__(self) -> int:
        return popcount(self.mask)

    def __repr__(self) -> str:
        return f"SquareSet({self.mask:#x})"

    def __sub__(self, other: IntoSquareSet):
        r = SquareSet(other)
        r.mask = self.mask & ~r.mask
        return r

    def __isub__(self, other: IntoSquareSet):
        self.mask &= ~SquareSet(other).mask
        return self

    def __or__(self, other: IntoSquareSet):
        r = SquareSet(other)
        r.mask |= self.mask
        return r

    def __ior__(self, other: IntoSquareSet):
        self.mask |= SquareSet(other).mask
        return self

    def __and__(self, other: IntoSquareSet):
        r = SquareSet(other)
        r.mask &= self.mask
        return r

    def __iand__(self, other: IntoSquareSet):
        self.mask &= SquareSet(other).mask
        return self

    def __xor__(self, other: IntoSquareSet):
        r = SquareSet(other)
        r.mask ^= self.mask
        return r

    def __ixor__(self, other: IntoSquareSet):
        self.mask ^= SquareSet(other).mask
        return self

    def __invert__(self):
        return SquareSet(~self.mask & BB_ALL)

    def __lshift__(self, shift: int):
        return SquareSet((self.mask << shift) & BB_ALL)

    def __rshift__(self, shift: int):
        return SquareSet(self.mask >> shift)

    def __ilshift__(self, shift: int):
        self.mask = (self.mask << shift) & BB_ALL
        return self

    def __irshift__(self, shift: int):
        self.mask >>= shift
        return self

    def __int__(self) -> int:
        return self.mask

    def __index__(self) -> int:
        return self.mask

    def __eq__(self, other: IntoSquareSet) -> bool:
        try:
            return self.mask == SquareSet(other).mask
        except (TypeError, ValueError):
            return NotImplemented

    def __str__(self) -> str:
        builder = []

        for square in SQUARES_180:
            mask = BB_SQUARES[square]
            builder.append("1" if self.mask & mask else ".")

            if not mask & BB_COLUMN_I:
                builder.append(" ")
            elif square != I0:
                builder.append("\n")

        return "".join(builder)

    def add(self, square: Square):
        """Adds a square to the set."""
        self.mask |= BB_SQUARES[square]

    def discard(self, square: Square):
        """Discards a square from the set."""
        self.mask &= ~BB_SQUARES[square]

    def isdisjoint(self, other: IntoSquareSet) -> bool:
        """Tests if the square sets are disjoint."""
        return not bool(self & other)

    def issubset(self, other: IntoSquareSet) -> bool:
        """Tests if this square set is a subset of another."""
        return not bool(self & ~SquareSet(other))

    def issuperset(self, other: IntoSquareSet) -> bool:
        """Tests if this square set is a superset of another."""
        return not bool(~self & other)

    def union(self, other: IntoSquareSet):
        return self | other

    def intersection(self, other: IntoSquareSet):
        return self & other

    def difference(self, other: IntoSquareSet):
        return self - other

    def symmetric_difference(self, other: IntoSquareSet):
        return self ^ other

    def update(self, *others: IntoSquareSet):
        for other in others:
            self |= other

    def intersection_update(self, *others: IntoSquareSet):
        for other in others:
            self &= other

    def difference_update(self, other: IntoSquareSet):
        self -= other

    def symmetric_difference_update(self, other: IntoSquareSet):
        self ^= other

    def copy(self):
        return SquareSet(self.mask)

    def remove(self, square: Square) -> None:
        """
        Removes a square from the set.

        :raises: :exc:`KeyError` if the given *square* was not in the set.
        """
        mask = BB_SQUARES[square]
        if self.mask & mask:
            self.mask ^= mask
        else:
            raise KeyError(square)

    def pop(self) -> Square:
        """
        Removes and returns a square from the set.

        :raises: :exc:`KeyError` if the set is empty.
        """
        if not self.mask:
            raise KeyError("pop from empty SquareSet")

        square = lsb(self.mask)
        self.mask &= (self.mask - 1)
        return square

    def clear(self):
        """Removes all elements from this set."""
        self.mask = BB_EMPTY

    def tolist(self) -> List[bool]:
        """Converts the set to a list of 64 bools."""
        result = [False] * 90
        for square in self:
            result[square] = True
        return result

    @classmethod
    def from_square(cls, square: Square):
        return cls(BB_SQUARES[square])