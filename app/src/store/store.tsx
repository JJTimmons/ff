import { applyMiddleware, createStore } from "redux";
import { composeWithDevTools } from "redux-devtools-extension";

import { IPlayer } from "../Player";
import { ITeam } from "../Team";
import reducers from "./reducers";

export interface IStoreState {
  activeTeam: number;
  currentPick: number; // index of current pick + 1
  draftDirection: number; // 1 or -1
  lastPickedPlayer: IPlayer | null;
  past: IStoreState | null;
  players: IPlayer[];
  selectedPlayer: IPlayer | null;
  teams: ITeam[];
  trackedTeam: number;
  undraftedPlayers: IPlayer[];
}

export const store = createStore(
  reducers,
  composeWithDevTools(applyMiddleware())
);
