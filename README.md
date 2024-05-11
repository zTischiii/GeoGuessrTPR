# Hilfestellung beim !party Befehl

Der `!party` Befehl ist ein zentraler Befehl in der Anwendung des Discord-Bots, der dazu dient, eine neue GeoGuessr-Party zu initiieren. Dieser Befehl akzeptiert drei Parameter, die es dem Benutzer ermöglichen, die Spielmodi, die Dauer des Spiels und die zu spielende Karte zu spezifizieren. Nachfolgend wird eine detaillierte Beschreibung der Syntax und der Funktionen dieses Befehls gegeben.

## Syntax des Befehls

Der Befehl folgt der folgenden Struktur:
`!party (Modi) [Zeit] {Karte}`


## Beschreibung der Parameter

### Modi

- **Syntax**: `(Modi)`
- **Beschreibung**: Eine durch Kommas getrennte Liste von Modi, die für das Spiel **deaktiviert** werden sollen. Die gültigen Modi sind "bewegen", "herumschauen" und "zoomen". Diese Modi bestimmen, welche Aktionen den Spielern während des Spiels nicht erlaubt sind.
- **Beispiel**: `(bewegen,zoomen)`

### Zeit

- **Syntax**: `[Zeit]`
- **Beschreibung**: Die Dauer des Spiels in Minuten und Sekunden. Die Zeit muss im Format `[M:S]` angegeben werden, wobei M für Minuten und S für Sekunden steht. Die Zeit muss zwischen 10 und 600 Sekunden liegen.
- **Beispiel**: `[1:30]` (1 Minute und 30 Sekunden)

### Karte

- **Syntax**: `{Karte}`
- **Beschreibung**: Der Name der Karte, auf der gespielt werden soll. Der Kartenname muss einer der vordefinierten Namen sein, wie "Welt", "Deutschland", "FamousPlaces", "Europa", "USA", "Japan", "EU", "UK", "Frankreich" oder "Spanien".
- **Beispiel**: `{Welt}`

## Beispiel für einen vollständigen Befehl

Ein vollständiger Befehl könnte wie folgt aussehen:
`!party (bewegen,zoomen) [1:30] {Welt}`

Dieser Befehl würde eine GeoGuessr-Party erstellen, bei der die Spieler sich bewegen und zoomen können, die Spielzeit 1 Minute und 30 Sekunden beträgt, und die Karte "Welt" verwendet wird.
