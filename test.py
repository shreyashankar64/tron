import tron, MyTronBot, unittest

#_____________________________________________________________________
# Board Helper Tests
#

class BoardHelperTestCase(unittest.TestCase):
    
    def test_read_board(self):
        board = MyTronBot.read_board('maps/test-board.txt')
        self.assertEqual(board.width, 6, 'incorrect width')
        self.assertEqual(board.height, 4, 'incorrect height')
        self.assertEqual(board[1,1], tron.ME, 'expected ME')
        self.assertEqual(board[1,4], tron.THEM, 'expected THEM')
        self.assertEqual(board.me(), (1,1))
        self.assertEqual(board.them(), (1,4))
        self.assertEqual(board[1,2], tron.WALL, 'expected WALL')
        self.assertEqual(board[1,3], tron.FLOOR, 'expected FLOOR')

    def test_adjacent_nonwall(self):
        board = MyTronBot.read_board('maps/test-board.txt')
        self.assertEqual(MyTronBot.adjacent_floor(board, board.me()), [(2,1)])
        self.assertEqual(MyTronBot.adjacent_floor(board, board.them()), [(1,3)])
        
    def test_adjacent_floor(self):
        board = MyTronBot.read_board('maps/test-board.txt')
        self.assertEqual(MyTronBot.adjacent_floor(board, board.me()), [(2,1)])
        self.assertEqual(MyTronBot.adjacent_floor(board, board.them()), [(1,3)])

    def test_surrounding_offset_array(self):
        soa = MyTronBot.surrounding_offset_array()
        self.assertEqual(len(soa), 9)
        self.assertEqual(soa[0], (-1,-1))
        self.assertEqual(soa[4], (0,0))
        self.assertEqual(soa[8], (1,1))

    def test_offset(self):
        self.assertEquals(MyTronBot.offset((1,1),(1,1)),(2,2))
        self.assertEquals(MyTronBot.offset((3,4),(-1,-1)),(2,3))
        self.assertEquals(MyTronBot.offset((3,2),(1,0)),(4,2))
    
    def test_surrounding_nonfloor(self):
        board = MyTronBot.read_board('maps/test-board.txt')
        self.assertEquals(len(MyTronBot.surrounding_nonfloor(board,(1,2))),5)

    def move_made(self):
        board = MyTronBot.read_board('maps/test-board.txt')
        fn = lambda(a,b): MyTronBot.move_made(board, a, b)
        self.assertEquals(fn((1,1),(2,1)), tron.SOUTH)
        self.assertEquals(fn((2,1),(1,1)), tron.NORTH)
        self.assertEquals(fn((1,1),(1,2)), tron.EAST)
        self.assertEquals(fn((1,2),(1,1)), tron.WEST)
        
    def test_is_game_over(self):
        board = MyTronBot.read_board('maps/test-board.txt')
        self.assertFalse(MyTronBot.is_game_over(board))
        board.board[2] = '######'
        self.assertTrue(MyTronBot.is_game_over(board))
        
    def test_win_lose_or_draw(self):
        board = MyTronBot.read_board('maps/test-board.txt')
        self.assertEqual(MyTronBot.win_lose_or_draw(board, tron.ME), 0)
        self.assertEqual(MyTronBot.win_lose_or_draw(board, tron.THEM), 0)
        board.board[2] = '######'
        self.assertEqual(MyTronBot.win_lose_or_draw(board, tron.ME), -1)
        self.assertEqual(MyTronBot.win_lose_or_draw(board, tron.THEM), 1)

    def test_set_char(self):
        self.assertEqual(MyTronBot.set_char('abc',0,'d'), 'dbc')
        self.assertEqual(MyTronBot.set_char('abc',1,'d'), 'adc')
        self.assertEqual(MyTronBot.set_char('abc',2,'d'), 'abd')

    def test_try_move(self):
        board = MyTronBot.read_board('maps/test-board.txt')
        self.assertEquals(board.me(), (1,1))
        self.assertEquals(board.them(), (1,4))
        self.assertEquals(board[2,1], tron.FLOOR, 'should be FLOOR')
        next = MyTronBot.try_move(board, tron.ME, tron.SOUTH)
        self.assertEquals(next.me(), (2,1), 'should have changed')
        self.assertEquals(next.them(), (1,4), 'should not have changed')
        self.assertEquals(next[1,1], tron.WALL, 'should now be WALL')
        self.assertEquals(board.me(), (1,1), 'should not have changed')
        self.assertEquals(board.them(), (1,4), 'should not have changed')
        self.assertEquals(board[2,1], tron.FLOOR, 'should still be FLOOR')

    def test_opponent(self):
        self.assertEquals(MyTronBot.opponent(tron.ME), tron.THEM)
        self.assertEquals(MyTronBot.opponent(tron.THEM), tron.ME)

    def test_count_around(self):
        board = MyTronBot.read_board('maps/u.txt')
        self.assertEquals(MyTronBot.count_around(board, board.me()), 97)
        board = MyTronBot.read_board('maps/ring.txt')
        self.assertEquals(MyTronBot.count_around(board, board.me()), 131)
        board = MyTronBot.read_board('maps/test-board.txt')
        self.assertEquals(MyTronBot.count_around(board, board.me()), 4)

#_____________________________________________________________________
# AIMA Alpha-Beta Interface Test
#

class AlphaBetaTestCase(unittest.TestCase):

    def setUp(self):
        board = MyTronBot.read_board('maps/test-board.txt')
        self.game = MyTronBot.TronGame()
        self.state = MyTronBot.make_state(board, tron.ME)

    def test_legal_moves(self):
        self.assertEquals(self.game.legal_moves(self.state), [tron.SOUTH])
        next = self.game.make_move(tron.SOUTH, self.state)
        self.assertEquals(self.game.legal_moves(next), [tron.WEST])

    def test_make_move(self):
        next = self.state
        self.assertEquals(next.board.me(), (1,1))
        self.assertEquals(next.board.them(), (1,4))
        next = self.game.make_move(tron.SOUTH, next)
        self.assertEquals(next.board.me(), (2,1))
        self.assertEquals(next.board.them(), (1,4))
        next = self.game.make_move(tron.WEST, next)
        self.assertEquals(next.board.me(), (2,1))
        self.assertEquals(next.board.them(), (1,3))

    def test_utility(self):
        next = self.state
        self.assertEquals(self.game.utility(next, tron.ME), 0)
        self.assertEquals(self.game.utility(next, tron.THEM), 0)
        board = next.board
        board.board[2] = '######'
        self.assertEquals(self.game.utility(next, tron.ME), -1)
        self.assertEquals(self.game.utility(next, tron.THEM), 1)
        
    def test_terminal_test(self):
        next = self.state
        self.assertFalse(self.game.terminal_test(next))
        board = next.board
        board.board[2] = '######'
        self.assertTrue(self.game.terminal_test(next))
        
#_____________________________________________________________________
# Shortest Path Tests
#

class ShortestPathTestCase(unittest.TestCase):

    def test_shortest_path(self):
        maps = { 'maps/u.txt': 27,
                 'maps/ring.txt': 15,
                 'maps/huge-room.txt': 93,
                 'maps/empty-room.txt': 23,
                 'maps/test-board.txt': 4 }
        for m in maps:
            board = MyTronBot.read_board(m)
            path = MyTronBot.shortest_path(board, board.me(), board.them())
            expected = maps[m]
            actual = MyTronBot.moves_between(path)
            self.assertEquals(actual, expected)

#_____________________________________________________________________
# Run tests if script.
#

if __name__ == '__main__':
    unittest.main()
