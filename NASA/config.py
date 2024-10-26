class DriveLM:
  def __init__(self):    
    self.constants = {
      'action_type': [['velocity_action_num', 4],
                     ['direction_action_num', 3]],
      'total_action_num': 7,
      'condition_num': 36
    }
    
    self.predicate = {
      'NORMAL': 0,
      'FAST': 1,
      'SLOW': 2,
      'STOP': 3,
      'LEFT': 4,
      'RIGHT': 5,
      'STRAIGHT': 6,
      'SOLID_RED_LIGHT': 7,
      'SOLID_YELLOW_LIGHT': 8,
      'YELLOW_LEFT_ARROW_LIGHT': 9,
      'RED_LEFT_ARROW_LIGHT': 10,
      'MERGING_TRAFFIC_SIGN': 11,
      'NO_LEFT_TURN_SIGN': 12,
      'NO_RIGHT_TURN_SIGN': 13,
      'PEDESTRIAN_CROSSING_SIGN': 14,
      'STOP_SIGN': 15,
      'RED_YIELD_SIGN': 16,
      'SLOW_SIGN': 17,
      'SOLID_GREEN_LIGHT': 18,
      'DOUBLE_DASHED_WHITE_LINE_LEFT': 19,
      'DOUBLE_DASHED_WHITE_LINE_RIGHT': 20,
      'SINGLE_SOLID_WHITE_LINE_LEFT': 21,
      'SINGLE_SOLID_WHITE_LINE_RIGHT': 22,
      'DOUBLE_SOLID_WHITE_LINE_LEFT': 23,
      'DOUBLE_SOLID_WHITE_LINE_RIGHT': 24,
      'SINGLE_ZIGZAG_WHITE_LINE_LEFT': 25,
      'SINGLE_ZIGZAG_WHITE_LINE_RIGHT': 26,
      'SINGLE_SOLID_YELLOW_LINE_LEFT': 27,
      'SINGLE_SOLID_YELLOW_LINE_RIGHT': 28,
      'NORMAL_CS': 29,
      'FAST_CS': 30,
      'SLOW_CS': 31,
      'STOP_CS': 32,
      'LEFT_CS': 33,
      'RIGHT_CS': 34,
      'STRAIGHT_CS': 35,
      'NORMAL_LLM': 36,
      'FAST_LLM': 37,
      'SLOW_LLM': 38,
      'STOP_LLM': 39,
      'LEFT_LLM': 40,
      'RIGHT_LLM': 41,
      'STRAIGHT_LLM': 42
    }
      
    self.formulas = [      
      
      lambda args: 1 - args[self.predicate["SOLID_RED_LIGHT"]] + args[self.predicate["FAST"]] * \
                      (1 - args[self.predicate["FAST"]]), # SolidRedLight → ¬Fast
                      
      lambda args: 1 - args[self.predicate["SOLID_YELLOW_LIGHT"]] + args[self.predicate["FAST"]] * \
                      (1 - args[self.predicate["FAST"]]), # SolidYellowLight → ¬Fast
                      
      lambda args: 1 - args[self.predicate["YELLOW_LEFT_ARROW_LIGHT"]] + args[self.predicate["YELLOW_LEFT_ARROW_LIGHT"]] * \
                      (args[self.predicate["STOP"]] + args[self.predicate["SLOW"]] - \
                      args[self.predicate["STOP"]] * args[self.predicate["SLOW"]]),  # YellowLeftArrowLight → Stop ∨ Slow

      lambda args: 1 - args[self.predicate["RED_LEFT_ARROW_LIGHT"]] + args[self.predicate["RED_LEFT_ARROW_LIGHT"]] * \
                      (1 - args[self.predicate["LEFT"]]),  # RedLeftArrowLight → ¬Left
      
      lambda args: 1 - args[self.predicate["MERGING_TRAFFIC_SIGN"]] + args[self.predicate["MERGING_TRAFFIC_SIGN"]] * \
                     (1- args[self.predicate["FAST"]]),  # MergingTrafficSign → ¬Fast

      lambda args: 1 - args[self.predicate["NO_LEFT_TURN_SIGN"]] + args[self.predicate["NO_LEFT_TURN_SIGN"]] * \
                      (1 - args[self.predicate["LEFT"]]),  # NoLeftTurnSign → ¬Left

      lambda args: 1 - args[self.predicate["NO_RIGHT_TURN_SIGN"]] + args[self.predicate["NO_RIGHT_TURN_SIGN"]] * \
                      (1 - args[self.predicate["RIGHT"]]),  # NoRightTurnSign → ¬Right
      
      lambda args: 1 - args[self.predicate["RED_YIELD_SIGN"]] + args[self.predicate["RED_YIELD_SIGN"]] * \
                      (1-args[self.predicate["FAST"]]),  # RedYieldSign → ¬Fast  

      lambda args: 1 - args[self.predicate["SLOW_SIGN"]] + args[self.predicate["SLOW_SIGN"]] * \
                      (1 - args[self.predicate["FAST"]]),  # SlowSign → ¬Fast  
                      
      lambda args: 1 - args[self.predicate["SINGLE_SOLID_WHITE_LINE_LEFT"]] + args[self.predicate["SINGLE_SOLID_WHITE_LINE_LEFT"]] * \
                      (1 - args[self.predicate["LEFT"]]),  # SingleSolidWhiteLineLeft → ¬Left
                      
      lambda args: 1 - args[self.predicate["SINGLE_SOLID_WHITE_LINE_RIGHT"]] + args[self.predicate["SINGLE_SOLID_WHITE_LINE_RIGHT"]] * \
                      (1 - args[self.predicate["RIGHT"]]),  # SingleSolidWhiteLineRight → ¬Right
                      
      lambda args: 1 - args[self.predicate["DOUBLE_SOLID_WHITE_LINE_LEFT"]] + args[self.predicate["DOUBLE_SOLID_WHITE_LINE_LEFT"]] * \
                      (1 - args[self.predicate["LEFT"]]),  # DOUBLE_SOLID_WHITE_LINE_LEFT → ¬Left
                      
      lambda args: 1 - args[self.predicate["DOUBLE_SOLID_WHITE_LINE_RIGHT"]] + args[self.predicate["DOUBLE_SOLID_WHITE_LINE_RIGHT"]] * \
                      (1 - args[self.predicate["RIGHT"]]),  # DOUBLE_SOLID_WHITE_LINE_RIGHT → ¬Right

      lambda args: 1 - args[self.predicate["SINGLE_ZIGZAG_WHITE_LINE_LEFT"]] + args[self.predicate["SINGLE_ZIGZAG_WHITE_LINE_LEFT"]] * \
                      (1 - args[self.predicate["STOP"]]),  # SingleZigzagWhiteLineLeft → ¬Stop

      lambda args: 1 - args[self.predicate["SINGLE_ZIGZAG_WHITE_LINE_RIGHT"]] + args[self.predicate["SINGLE_ZIGZAG_WHITE_LINE_RIGHT"]] * \
                      (1 - args[self.predicate["STOP"]]),  # SingleZigzagWhiteLineRight → ¬Stop 
                      
      lambda args: 1 - args[self.predicate["NORMAL_CS"]] + args[self.predicate["NORMAL_CS"]] * \
                      args[self.predicate["NORMAL"]],  # NORMAL_CS → NORMAL
                      
      lambda args: 1 - args[self.predicate["FAST_CS"]] + args[self.predicate["FAST_CS"]] * \
                      args[self.predicate["FAST"]],  # FAST_CS → FAST
                      
      lambda args: 1 - args[self.predicate["SLOW_CS"]] + args[self.predicate["SLOW_CS"]] * \
                      args[self.predicate["SLOW"]],  # SLOW_CS → SLOW
                      
      lambda args: 1 - args[self.predicate["STOP_CS"]] + args[self.predicate["STOP_CS"]] * \
                      args[self.predicate["STOP"]],  # STOP_CS → STOP 
                      
      lambda args: 1 - args[self.predicate["LEFT_CS"]] + args[self.predicate["LEFT_CS"]] * \
                      args[self.predicate["LEFT"]],  # LEFT_CS → LEFT
                      
      lambda args: 1 - args[self.predicate["RIGHT_CS"]] + args[self.predicate["RIGHT_CS"]] * \
                      args[self.predicate["RIGHT"]],  # RIGHT_CS → RIGHT
                      
      lambda args: 1 - args[self.predicate["STRAIGHT_CS"]] + args[self.predicate["STRAIGHT_CS"]] * \
                      args[self.predicate["STRAIGHT"]],  # STRAIGHT_CS → STRAIGHT
                      
      lambda args: 1 - args[self.predicate["NORMAL_LLM"]] + args[self.predicate["NORMAL_LLM"]] * \
                      args[self.predicate["NORMAL"]],  # NORMAL_LLM → NORMAL
                      
      lambda args: 1 - args[self.predicate["FAST_LLM"]] + args[self.predicate["FAST_LLM"]] * \
                      args[self.predicate["FAST"]],  # FAST_LLM → FAST
                      
      lambda args: 1 - args[self.predicate["SLOW_LLM"]] + args[self.predicate["SLOW_LLM"]] * \
                      args[self.predicate["SLOW"]],  # SLOW_LLM → SLOW
                      
      lambda args: 1 - args[self.predicate["STOP_LLM"]] + args[self.predicate["STOP_LLM"]] * \
                      args[self.predicate["STOP"]],  # STOP_LLM → STOP
                      
      lambda args: 1 - args[self.predicate["LEFT_LLM"]] + args[self.predicate["LEFT_LLM"]] * \
                      args[self.predicate["LEFT"]],  # LEFT_LLM → LEFT
                      
      lambda args: 1 - args[self.predicate["RIGHT_LLM"]] + args[self.predicate["RIGHT_LLM"]] * \
                      args[self.predicate["RIGHT"]],  # RIGHT_LLM → RIGHT
                      
      lambda args: 1 - args[self.predicate["STRAIGHT_LLM"]] + args[self.predicate["STRAIGHT_LLM"]] * \
                      args[self.predicate["STRAIGHT"]]  # STRAIGHT_LLM → STRAIGHT 
    ] 
    
    self.possible_worlds = [
      (self.predicate["NORMAL"], self.predicate["LEFT"]),
      (self.predicate["NORMAL"], self.predicate["RIGHT"]),
      (self.predicate["NORMAL"], self.predicate["STRAIGHT"]),
      (self.predicate["FAST"], self.predicate["LEFT"]),
      (self.predicate["FAST"], self.predicate["RIGHT"]),
      (self.predicate["FAST"], self.predicate["STRAIGHT"]),
      (self.predicate["SLOW"], self.predicate["LEFT"]),
      (self.predicate["SLOW"], self.predicate["RIGHT"]),
      (self.predicate["SLOW"], self.predicate["STRAIGHT"]),
      (self.predicate["STOP"], self.predicate["LEFT"]),
      (self.predicate["STOP"], self.predicate["RIGHT"]),
      (self.predicate["STOP"], self.predicate["STRAIGHT"]),
    ]
    
    
class AirTaxi:
  def __init__(self):
    self.constants = {
      'action_type': [['action_num', 7]],
      'total_action_num': 7,
      'condition_num': 14
    }
    
    self.action_predicate = {
      'Accelerate': 0,
      'Decelerate': 1,
      'Stop': 2,
      'Right': 3,
      'Left': 4,
      'Up': 5,
      'Down': 6,
    }
    
    self.observed_predicate = {
      'Cruising': 7,
      'Landing': 8,
      'Altitude_above_50': 9,
      'Altitude_below_50': 10,
      'Velocity_less_than_2': 11,
      'Velocity_more_than_2': 12,
      'Obstacles_in_1m_radius': 13
    }
    
    self.past_action_predicate = {
      'Accelerate_P': 14,
      'Decelerate_P': 15,
      'Stop_P': 16,
      'Right_P': 17,
      'Left_P': 18,
      'Up_P': 19,
      'Down_P': 20,
    }
    
    self.formulas = [
      lambda args: 1 - (args[self.observed_predicate["Cruising"]] * args[self.observed_predicate["Altitude_below_50"]]) + \
              (args[self.observed_predicate["Cruising"]] * args[self.observed_predicate["Altitude_below_50"]] * args[self.action_predicate["Up"]]), # Cruising and Altitude_below_50 -> Up
      
      lambda args: 1 - (args[self.observed_predicate["Landing"]] * args[self.observed_predicate["Altitude_above_50"]]) + \
              (args[self.observed_predicate["Landing"]] * args[self.observed_predicate["Altitude_above_50"]] * args[self.action_predicate["Down"]]), # Landing and Altitude_above_50 -> Down
              
      lambda args: 1 - args[self.observed_predicate["Obstacles_in_1m_radius"]] + \
              args[self.observed_predicate["Obstacles_in_1m_radius"]] * args[self.action_predicate["Stop"]], # Obstacles_in_1m_radius -> Stop

      lambda args: 1 - (args[self.observed_predicate["Landing"]] * args[self.observed_predicate["Velocity_more_than_2"]]) + \
              (args[self.observed_predicate["Landing"]] * args[self.observed_predicate["Velocity_more_than_2"]] * args[self.action_predicate["Decelerate"]]), # Landing and Velocity_more_than_2 -> Decelerate

      lambda args: 1 - args[self.past_action_predicate["Accelerate_P"]] + \
              args[self.past_action_predicate["Accelerate_P"]] * (args[self.action_predicate["Accelerate"]] + args[self.action_predicate["Stop"]]), # Accelerate_P -> Accelerate ∨ Stop
              
      lambda args: 1 - args[self.past_action_predicate["Decelerate_P"]] + \
              args[self.past_action_predicate["Decelerate_P"]] * (args[self.action_predicate["Decelerate"]] + args[self.action_predicate["Stop"]]), # Decelerate_P -> Decelerate ∨ Stop
              
      lambda args: 1 - args[self.past_action_predicate["Right_P"]] + \
              args[self.past_action_predicate["Right_P"]] * (args[self.action_predicate["Right"]] + args[self.action_predicate["Stop"]]), # Right_P -> Right ∨ Stop
              
      lambda args: 1 - args[self.past_action_predicate["Left_P"]] + \
              args[self.past_action_predicate["Left_P"]] * (args[self.action_predicate["Left"]] + args[self.action_predicate["Stop"]]), # Left_P -> Left ∨ Stop
              
      lambda args: 1 - args[self.past_action_predicate["Up_P"]] + \
              args[self.past_action_predicate["Up_P"]] * (args[self.action_predicate["Up"]] + args[self.action_predicate["Stop"]]), # Up_P -> Up ∨ Stop
              
      lambda args: 1 - args[self.past_action_predicate["Down_P"]] + \
              args[self.past_action_predicate["Down_P"]] * (args[self.action_predicate["Down"]] + args[self.action_predicate["Stop"]]), # Down_P -> Down ∨ Stop
    ]
    
