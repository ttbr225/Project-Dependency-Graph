{
  description = "LLM-powered task dependency mapper";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          google-generativeai
          graphviz        # the Python bindings
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
            pkgs.graphviz   # the system binary (provides `dot`) — the bit pip can't give you
          ];
          shellHook = ''
            echo "dependency-mapper dev shell ready."
            echo "Set your key:  export GEMINI_API_KEY=..."
          '';
        };
      });
}