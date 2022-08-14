// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SimpleStorage {
    // this will get initialized to 0!
    uint256 balance;
    string coin;

    struct People {
        uint256 p_balance;
        string p_coin;
        string p_name;
    }

    People[] public peeps;
    mapping(string => uint256) public name_to_balance;

    function store(uint256 _balance) public {
        balance = _balance;
    }

    function retrieve() public view returns (uint256) {
        return balance;
    }

    function addPerson(
        string memory _name,
        uint256 _balance,
        string memory _coin
    ) public {
        peeps.push(People(_balance, _coin, _name));
        name_to_balance[_name] = _balance;
    }

    function getPerson() public view returns (People[] memory) {
        return peeps;
    }

    function getPerson1(uint256 i)
        public
        view
        returns (
            uint256,
            string memory,
            string memory
        )
    {
        if (i < peeps.length - 1) {
            return (peeps[i].p_balance, peeps[i].p_coin, peeps[i].p_name);
        }
        return (0, "", "");
    }
}
